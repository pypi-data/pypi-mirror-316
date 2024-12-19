from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from strenum import LowercaseStrEnum as StrEnum
from pickle import PickleError
import sys
import struct
from functools import partial
from typing import Callable, List, Optional, TypedDict, TYPE_CHECKING
import tempfile
import os
import importlib.util
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from subprocess import run
import logging

import ibis
from tqdm import tqdm
import numpy as np
import pandas as pd
from google.protobuf.message import Message
import pyarrow
from pyarrow.flight import FlightDescriptor
from turboml.common.concurrent import multiprocessing_enabled, get_executor_pool_class
from .models import (
    DataDrift,
    Dataset,
    DatasetSchema,
    SchemaType,
    DatasetRegistrationRequest,
    DatasetRegistrationResponse,
    validate_dataframe_field_names,
)
from .feature_engineering import (
    FeatureEngineering,
    get_features,
)
from .api import api
from .env import CONFIG
from .protos import output_pb2
from .internal import TbItertools, TbPyArrow

if TYPE_CHECKING:
    from google.protobuf import message


logger = logging.getLogger(__name__)


class DatasetType(StrEnum):
    INPUT_TOPIC = "input_topic"
    OUTPUT = "output"
    TARGET_DRIFT = "target_drift"
    UNIVARIATE_DRIFT = "univariate_drift"
    MULTIVARIATE_DRIFT = "multivariate_drift"


class Record(TypedDict):
    offset: int
    record: bytes


def _get_raw_msgs(dataset_type: DatasetType, name: str, **kwargs):
    """
    Returns a dataframe of type [offset: int, record: bytes] for the dataset
    """
    if dataset_type == DatasetType.UNIVARIATE_DRIFT:
        numeric_feature = kwargs.get("numeric_feature")
        if numeric_feature is None:
            raise ValueError("numeric_feature is required for univariate drift")
        name = f"{name}:{numeric_feature}"
    if dataset_type == DatasetType.MULTIVARIATE_DRIFT:
        label = kwargs.get("label")
        if label is None:
            raise ValueError("label is required for multivariate drift")
        name = f"{name}:{label}"
    arrow_descriptor = pyarrow.flight.Ticket(f"{dataset_type.value}:{name}")
    client = pyarrow.flight.connect(f"{CONFIG.ARROW_SERVER_ADDRESS}")
    TbPyArrow.wait_for_available(client)
    reader = client.do_get(
        arrow_descriptor,
        options=pyarrow.flight.FlightCallOptions(headers=api.arrow_headers),
    )
    LOG_FREQUENCY_SEC = 3
    last_log_time = 0
    yielded_total = 0
    yielded_batches = 0
    start_time = datetime.now().timestamp()
    while True:
        table = reader.read_chunk().data
        df = TbPyArrow.arrow_table_to_pandas(table)
        if df.empty:
            logger.info(
                f"Yielded {yielded_total} records ({yielded_batches} batches) in {datetime.now().timestamp() - start_time:.0f} seconds"
            )
            break
        yielded_total += len(df)
        yielded_batches += 1
        if (now := datetime.now().timestamp()) - last_log_time > LOG_FREQUENCY_SEC:
            logger.info(
                f"Yielded {yielded_total} records ({yielded_batches} batches) in {now - start_time:.0f} seconds"
            )
            last_log_time = now
        assert isinstance(df, pd.DataFrame)
        yield df


PROTO_PREFIX_BYTE_LEN = 6


def _records_to_proto_messages(
    df: pd.DataFrame,
    proto_msg: Callable[[], message.Message],
) -> tuple[list[int], list[message.Message]]:
    offsets = []
    proto_records = []
    for _, offset_message in df.iterrows():
        offset, message = offset_message["offset"], offset_message["record"]
        assert isinstance(message, bytes)
        proto = proto_msg()
        proto.ParseFromString(message[PROTO_PREFIX_BYTE_LEN:])
        offsets.append(offset)
        proto_records.append(proto)
    return offsets, proto_records


class RecordList(TypedDict):
    offsets: list[int]
    records: list[message.Message]


# HACK: Since it is observed that the ProcessPoolExecutor fails to pickle proto messages under
# certain (not yet understood) conditions, we switch to the ThreadPoolExecutor upon encountering
# such an error.
# Ref: https://turboml.slack.com/archives/C07FM09V0MA/p1729082597265189


def get_proto_msgs(
    dataset_type: DatasetType,
    name: str,
    proto_msg: Callable[[], message.Message],
    **kwargs,
    # limit: int = -1
) -> list[Record]:
    executor_pool_class = get_executor_pool_class()
    try:
        return _get_proto_msgs(
            dataset_type, name, proto_msg, executor_pool_class, **kwargs
        )
    except PickleError as e:
        if not multiprocessing_enabled():
            raise e
        logger.warning(
            f"Failed to pickle proto message class {proto_msg}: {e}. Retrying with ThreadPoolExecutor"
        )

        return _get_proto_msgs(
            dataset_type, name, proto_msg, ThreadPoolExecutor, **kwargs
        )


def _get_proto_msgs(
    dataset_type: DatasetType,
    name: str,
    proto_msg: Callable[[], message.Message],
    executor_cls: type[ProcessPoolExecutor | ThreadPoolExecutor],
    **kwargs,
) -> list[Record]:
    messages_generator = _get_raw_msgs(dataset_type, name, **kwargs)
    offsets = []
    records = []
    with executor_cls(max_workers=os.cpu_count()) as executor:
        futures: list[Future[tuple[list[int], list[message.Message]]]] = []
        for df in messages_generator:
            future = executor.submit(
                _records_to_proto_messages,
                df,
                proto_msg,
            )
            futures.append(future)
        for future in futures:
            offsets_chunk, records_chunk = future.result()
            offsets.extend(offsets_chunk)
            records.extend(records_chunk)

    ret = []
    for i, record in zip(offsets, records, strict=True):
        ret.append({"offset": i, "record": record})
    return ret


class _Internal:
    @staticmethod
    def _infer_object_column_type(columns: pd.Series) -> Optional[str]:
        try:
            if isinstance(columns[0], str) and columns.astype(str) is not None:
                return "string"
        except UnicodeDecodeError:
            pass

        try:
            if isinstance(columns[0], bytes) and columns.astype(bytes) is not None:
                return "bytes"
        except TypeError:
            pass

        return None

    @staticmethod
    def _map_pandas_to_proto_dtype(df, column_name):
        match df[column_name].dtype:
            case np.int32:
                proto_dtype = "int32"
            case np.int64:
                proto_dtype = "int64"
            case np.float32:
                proto_dtype = "float"
            case np.float64:
                proto_dtype = "double"
            case np.bool_:
                proto_dtype = "bool"
            case np.bytes_:
                proto_dtype = "bytes"
            case np.object_:
                # At this point we're not sure of the type: pandas by default
                # interprets both `bytes` and `str` into `object_` columns
                column = df[column_name]
                if not isinstance(column, pd.Series):
                    raise ValueError(
                        f"Unsupported dtype: column {column_name}, type {type(column)}"
                    )
                proto_dtype = _Internal._infer_object_column_type(column)
                if proto_dtype is None:
                    raise ValueError(f"Unsupported dtype for column {column_name}")
            case _:
                raise ValueError(f"Unsupported dtype: {df[column_name].dtype}")
        return proto_dtype

    @staticmethod
    def register_dataset(
        df: pd.DataFrame, dataset_id: str, key_field: str
    ) -> DatasetSchema:
        """
        Retrieve or register a Protocol Buffers (protobuf) schema for a given DataFrame and dataset_id.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be represented in the protobuf schema.
            dataset_id (str): The dataset_id or name associated with the protobuf schema.
            key_field (str): The primary key used to register dataset.

        Returns:
            Union[Schema, RegisteredSchema]: If the schema already exists in the Schema Registry, return the schema.
            If the schema doesn't exist, create a new schema based on the DataFrame structure,
            register it in the Schema Registry, and return the registered schema.
        Raises:
            SchemaRegistryError: If an unexpected error occurs during schema retrieval or registration.
        """
        schema_body = get_proto_schema_from_df(df, dataset_id)
        logger.debug(
            f"Registering dataset {dataset_id} with schema_body: {schema_body} and key_field: {key_field}"
        )
        payload = DatasetRegistrationRequest(
            dataset_id=dataset_id,
            schema_body=schema_body,
            schema_type=SchemaType.PROTOBUF,
            key_field=key_field,
        )

        response = api.post(endpoint="dataset", json=payload.model_dump())
        if response.status_code not in range(200, 299):
            raise Exception(
                f"Failed to register dataset {dataset_id}: {response.json()}"
            )

        return DatasetRegistrationResponse(**response.json()).registered_schema


def get_proto_schema_from_df(df: pd.DataFrame, message_name: str) -> str:
    """Create a Protocol Buffers (protobuf) schema from Pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be represented in the protobuf schema.
        message_name (str): The schema message name.

    Returns:
        str: A string representing the protobuf schema.
    """
    validate_dataframe_field_names(df)
    field_decls = []
    for i, cname in enumerate(df.columns):
        proto_dtype = _Internal._map_pandas_to_proto_dtype(df, cname)
        field_decls.append(f"optional {proto_dtype} {cname} = {i + 1};")
    NEWLINE = "\n"
    proto = f"""syntax = "proto2";
message {message_name} {{
{NEWLINE.join(field_decls)}
}}"""
    return proto


def create_protobuf_from_row_tuple(
    row: tuple,
    fields: List[str],
    proto_cls: Callable[[], message.Message],
    prefix: bytes,
):
    """Create a Protocol Buffers (protobuf) message by populating its fields with values from a tuple of row data.

    Args:
        row (Iterable): An iterable representing a row of data. Each element corresponds to a field in the protobuf message.
        fields (List[str]): A list of field names corresponding to the fields in the protobuf message class.
        proto_cls (type): The protobuf message class to instantiate.
        prefix (str): A string prefix to be concatenated with the serialized message.

    Returns:
        str: A string representing the serialized protobuf message with the specified prefix.
    """
    my_msg = proto_cls()
    for i, field in enumerate(fields):
        value = row[i]

        try:
            setattr(my_msg, field, value)
        except TypeError as e:
            logger.error(
                f"Error setting field '{field}' with value '{value}' in '{row}': {e}"
            )
            raise

    return prefix + my_msg.SerializeToString()


def create_protobuf_from_row_dict(
    row: dict,
    proto_cls: Callable[[], message.Message],
    prefix: bytes,
):
    """Create a Protocol Buffers (protobuf) message by populating its fields with values a from dictionary row of data.

    Args:
        row (Iterable): An iterable representing a row of data. Each element corresponds to a field in the protobuf message.
        proto_cls (type): The protobuf message class to instantiate.
        prefix (str): A string prefix to be concatenated with the serialized message.

    Returns:
        str: A string representing the serialized protobuf message with the specified prefix.
    """
    my_msg = proto_cls()
    for field, value in row.items():
        try:
            setattr(my_msg, field, value)
        except TypeError as e:
            logger.error(
                f"Error setting field '{field}' with value '{value}' in '{row}': {e}"
            )
            raise

    return prefix + my_msg.SerializeToString()


def get_protobuf_class(class_name: str, schema: str):
    """Generated a python class from a Protocol Buffers (protobuf) message schema.

    Args:
        class_name: protobuf class name for the schema.
        schema: protobuf schema.

    Returns:
        class type: protobuf python class derived from protobuf `Message` abstract class.
    """
    module_name = f'{class_name.replace("-", "_")}_pb2'
    if module_name not in sys.modules:
        with tempfile.TemporaryDirectory(prefix="turboml_") as tempdir:
            filename = os.path.join(tempdir, f"{class_name}.proto")
            with open(filename, "w") as f:
                _ = f.write(schema)
            dirname = os.path.dirname(filename)
            basename = os.path.basename(filename)
            run(
                [
                    "protoc",
                    f"--python_out={dirname}",
                    f"--proto_path={dirname}",
                    basename,
                ],
                check=True,
            )
            module_path = os.path.join(dirname, module_name + ".py")
            module_spec = importlib.util.spec_from_file_location(
                module_name, module_path
            )
            if module_spec is None:
                raise ValueError(f"Could not import {module_name}")
            module = importlib.util.module_from_spec(module_spec)
            sys.modules[module_name] = module
            module_spec.loader.exec_module(module)
    else:
        module = sys.modules[module_name]

    messageClasses = [
        v
        for v in vars(module).values()
        if isinstance(v, type) and issubclass(v, Message)
    ]
    messageClass = messageClasses[0]
    return messageClass


def upload_df(
    dataset_id: str,
    df: pd.DataFrame,
    schema: DatasetSchema,
    protoMessageClass: Optional[Message] = None,
) -> None:
    """Upload data from a DataFrame to a dataset after preparing and serializing it as Protocol Buffers (protobuf) messages.

    Args:
        dataset_id (str): The Kafka dataset_id to which the data will be sent.
        df (pd.DataFrame): The DataFrame containing the data to be uploaded.
        schema (Schema): Dataset schema.
        protoMessageClass (Optional(Message)): Protobuf Message Class to use. Generated if not provided.
    """
    if protoMessageClass is None:
        protoMessageClass = get_protobuf_class(dataset_id, schema.schema_body)

    fields = df.columns.tolist()
    prefix = struct.pack("!xIx", schema.id)
    descriptor = FlightDescriptor.for_command(f"produce:{dataset_id}")
    client = pyarrow.flight.connect(f"{CONFIG.ARROW_SERVER_ADDRESS}")
    TbPyArrow.wait_for_available(client)
    pa_schema = pyarrow.schema([("value", pyarrow.binary())])
    writer, _ = client.do_put(
        descriptor,
        pa_schema,
        options=pyarrow.flight.FlightCallOptions(headers=api.arrow_headers),
    )

    partial_converter_func = partial(
        create_protobuf_from_row_tuple,
        fields=fields,
        proto_cls=protoMessageClass,
        prefix=prefix,
    )

    logger.info(f"Uploading {df.shape[0]} rows to dataset {dataset_id}")

    executor_pool_class = get_executor_pool_class()
    try:
        _upload_df_batch(df, executor_pool_class, partial_converter_func, writer)
    except (PickleError, ModuleNotFoundError) as e:
        if not multiprocessing_enabled():
            raise e
        logger.warning(
            f"Dataframe batch update failed due to exception {e}. Retrying with ThreadPoolExecutor"
        )
        _upload_df_batch(df, ThreadPoolExecutor, partial_converter_func, writer)

    logger.info("Upload complete. Waiting for server to process messages.")
    writer.close()


def _upload_df_batch(
    df: pd.DataFrame,
    executor_pool_class: type[ProcessPoolExecutor | ThreadPoolExecutor],
    partial_func,
    writer,
):
    with executor_pool_class(max_workers=os.cpu_count()) as executor:
        data_iterator = executor.map(
            partial_func,
            df.itertuples(index=False, name=None),
            chunksize=1024,
        )

        CHUNK_SIZE = 1024
        row_length = df.shape[0]
        with tqdm(
            total=row_length, desc="Progress", unit="rows", unit_scale=True
        ) as pbar:
            for messages in TbItertools.chunked(data_iterator, CHUNK_SIZE):
                batch = pyarrow.RecordBatch.from_arrays([messages], ["value"])
                writer.write(batch)
                pbar.update(len(messages))


class BaseDataset(ABC):
    @abstractmethod
    def get_input_fields(
        self,
        numerical_fields: list = None,
        categorical_fields: list = None,
        textual_fields: list = None,
        imaginal_fields: list = None,
        time_field: str = None,
    ) -> Inputs:
        pass

    @abstractmethod
    def get_label_field(self, label_field: str) -> Labels:
        pass


class PandasDataset(BaseDataset):
    def __init__(  # noqa: C901
        self,
        dataframe: Optional[pd.DataFrame] = None,
        dataset_name: Optional[str] = None,
        key_field: Optional[str] = None,
        streaming: bool = True,
        upload: bool = False,
    ) -> None:
        if dataframe is not None:
            validate_dataframe_field_names(dataframe)
        if not streaming and upload:
            raise Exception(
                "The 'upload' parameter is set to True, but the dataset is not streaming"
            )
        self.dataset_id = dataset_name
        self.key_field = key_field
        self.feature_engineering = FeatureEngineering(self.dataset_id, not streaming)
        self.streaming = streaming

        if dataframe is not None:
            if key_field is None:
                raise Exception("The key_field is required.")

        if upload:
            if dataframe is None:
                raise Exception(
                    "The 'upload' parameter is set to True, but no dataframe was provided"
                )
            if dataset_name is None:
                raise Exception(
                    "The 'upload' parameter is set to True, but no dataset was provided"
                )
            self.schema = _Internal.register_dataset(dataframe, dataset_name, key_field)
            upload_df(dataset_name, dataframe, self.schema)
        if not streaming and dataframe is None:
            raise Exception("No dataframe provided for non-streaming dataset")
        if dataframe is None:
            dataset = api.get(endpoint=f"dataset?dataset_id={self.dataset_id}").json()
            dataset = Dataset(**dataset)
            self.key_field = dataset.key
            self.schema = self._get_registered_schema()
            self.input_df = get_features(self.dataset_id)
            self.feature_engineering.local_features_df = self.input_df.copy()
            self.feature_engineering.all_materialized_features_df = self.input_df.copy()
        else:
            self.input_df = dataframe

        self.feature_engineering.local_features_df = self.input_df.copy()

        if self.streaming:
            self.feature_engineering.all_materialized_features_df = get_features(
                self.dataset_id
            )
        else:
            self.feature_engineering.all_materialized_features_df = self.input_df.copy()

    def sync_features(self):
        if not self.streaming:
            raise Exception("Refresh not supported for non-streaming dataset.")
        self.input_df = get_features(self.dataset_id)
        self.feature_engineering.local_features_df = self.input_df.copy()
        self.feature_engineering.all_materialized_features_df = self.input_df.copy()

    def upload_df(self, dataframe: pd.DataFrame):
        if not self.streaming:
            raise Exception("Upload not supported for non-streaming dataset.")
        if self.schema is None:
            self.schema = self._get_registered_schema()
        upload_df(self.dataset_id, dataframe, self.schema)

    def _get_registered_schema(self):
        if not self.streaming:
            raise Exception("No registered schema for non-streaming dataset.")
        if self.dataset_id is None:
            raise Exception("Dataset id not set.")
        schema_json = api.get(endpoint=f"dataset/{self.dataset_id}/schema").json()
        schema = DatasetSchema(**schema_json)
        return schema

    def _get_df(self):
        if self.streaming:
            return self.feature_engineering.get_materialized_features()
        else:
            return self.feature_engineering.get_local_features()

    def get_input_fields(
        self,
        numerical_fields: list | None = None,
        categorical_fields: list | None = None,
        textual_fields: list | None = None,
        imaginal_fields: list | None = None,
        time_field: str | None = None,
    ):
        # Normalize
        if numerical_fields is None:
            numerical_fields = []
        if categorical_fields is None:
            categorical_fields = []
        if textual_fields is None:
            textual_fields = []
        if imaginal_fields is None:
            imaginal_fields = []

        dataframe = self._get_df()

        for field in (
            numerical_fields + categorical_fields + textual_fields + imaginal_fields
        ):
            if field not in dataframe.columns:
                raise ValueError(f"Field '{field}' is not present in the dataset.")
        if time_field is not None:
            if time_field not in dataframe.columns:
                raise ValueError(f"Field '{time_field}' is not present in the dataset.")

        return Inputs(
            dataframe=dataframe,
            key_field=self.key_field,
            numerical_fields=numerical_fields,
            categorical_fields=categorical_fields,
            textual_fields=textual_fields,
            imaginal_fields=imaginal_fields,
            time_field=time_field,
            dataset_id=self.dataset_id,
        )

    def register_univariate_drift(
        self, numerical_field: str, label: Optional[str] = None
    ):
        if not self.streaming:
            raise Exception("Method not supported on non-streaming datasets")
        assert self.dataset_id is not None

        if not numerical_field:
            raise Exception("Numerical field not specified")

        payload = DataDrift(label=label, numerical_fields=[numerical_field])
        api.put(endpoint=f"dataset/{self.dataset_id}/drift", json=payload.model_dump())

    def register_multivariate_drift(self, numerical_fields: list[str], label: str):
        if not self.streaming:
            raise Exception("Method not supported on non-streaming datasets")
        # TODO: We should really split types for streaming and non-streaming datasets :)
        assert self.dataset_id is not None

        payload = DataDrift(label=label, numerical_fields=numerical_fields)
        api.put(endpoint=f"dataset/{self.dataset_id}/drift", json=payload.model_dump())

    def get_univariate_drift(
        self,
        label: Optional[str] = None,
        numerical_field: Optional[str] = None,
        limit: int = -1,
    ):
        if not self.streaming:
            raise Exception("Method not supported on non-streaming datasets")

        if numerical_field is None and label is None:
            raise Exception("Numerical field and label both cannot be None")

        assert self.dataset_id is not None

        drift_label = (
            self.get_data_drift_label([numerical_field]) if label is None else label
        )

        return get_proto_msgs(
            DatasetType.UNIVARIATE_DRIFT,
            self.dataset_id,
            output_pb2.Output,
            numeric_feature=drift_label,
        )

    def get_multivariate_drift(
        self,
        label: Optional[str] = None,
        numerical_fields: Optional[list[str]] = None,
        limit: int = -1,
    ):
        if not self.streaming:
            raise Exception("Method not supported on non-streaming datasets")

        if numerical_fields is None and label is None:
            raise Exception("Numerical fields and label both cannot be None")

        assert self.dataset_id is not None

        drift_label = (
            self.get_data_drift_label(numerical_fields) if label is None else label
        )

        return get_proto_msgs(
            DatasetType.MULTIVARIATE_DRIFT,
            self.dataset_id,
            output_pb2.Output,
            label=drift_label,
        )

    def get_data_drift_label(self, numerical_fields: list[str]):
        payload = DataDrift(numerical_fields=numerical_fields, label=None)

        drift_label = api.get(
            f"dataset/{self.dataset_id}/drift_label", json=payload.model_dump()
        ).json()["label"]

        return drift_label

    def get_label_field(self, label_field: str):
        if not label_field or label_field not in self.input_df.columns:
            raise Exception("Label field not specified or not found in the dataframe")
        return Labels(
            dataframe=self.input_df,
            key_field=self.key_field,
            label_field=label_field,
            dataset_id=self.dataset_id,
        )

    def to_ibis(self):
        """
        Converts the dataset into an Ibis table.

        Returns:
            ibis.expr.types.Table: An Ibis in-memory table representing the features
            associated with the given dataset_id.

        Raises:
            Exception: If any error occurs during the retrieval of the table name,
            features, or conversion to Ibis table.
        """
        try:
            df = get_features(self.dataset_id)
            return ibis.memtable(df, name=self.dataset_id)
        except Exception as e:
            raise e

    def __repr__(self):
        return f"PandasDataset({', '.join(f'{key}={value}' for key, value in vars(self).items())})"


class Inputs:
    def __init__(
        self,
        dataframe: pd.DataFrame,
        key_field: str,
        numerical_fields: list | None = None,
        categorical_fields: Optional[list] = None,
        textual_fields: Optional[list] = None,
        imaginal_fields: Optional[list] = None,
        time_field: Optional[str] = None,
        dataset_id: Optional[str] = None,
    ) -> None:
        # Normalize
        if numerical_fields is None:
            numerical_fields = []
        if categorical_fields is None:
            categorical_fields = []
        if textual_fields is None:
            textual_fields = []
        if imaginal_fields is None:
            imaginal_fields = []

        self.dataset_id = dataset_id
        self.key_field = key_field
        self.textual_fields = textual_fields
        self.imaginal_fields = imaginal_fields
        self.numerical_fields = numerical_fields
        self.categorical_fields = categorical_fields
        self.time_field = time_field

        # acc all columns to keep
        all_fields = set(
            [key_field]
            + numerical_fields
            + categorical_fields
            + textual_fields
            + imaginal_fields
            + ([time_field] if time_field else [])
        )
        self.dataframe = dataframe[list(all_fields)].copy()
        self.validate_fields(dataframe)

    def __repr__(self):
        return f"Inputs({', '.join(f'{key}={value}' for key, value in vars(self).items())})"

    def _validate_time_field(self, dataframe: pd.DataFrame):
        if self.time_field:
            time_field_is_datetime64 = pd.api.types.is_datetime64_any_dtype(
                dataframe[self.time_field]
            )
            if not time_field_is_datetime64:
                raise ValueError(
                    f"Field '{self.time_field}' is not of a datetime type."
                )

    def validate_fields(self, dataframe: pd.DataFrame):
        validate_dataframe_field_names(dataframe)
        all_fields = (
            self.numerical_fields
            + self.categorical_fields
            + self.textual_fields
            + self.imaginal_fields
        )
        if self.time_field:
            all_fields.append(self.time_field)

        all_fields.append(self.key_field)

        for field in all_fields:
            if field not in dataframe.columns:
                raise ValueError(f"Field '{field}' is not present in the dataframe.")

        for field in self.numerical_fields:
            if not pd.api.types.is_numeric_dtype(dataframe[field]):
                raise ValueError(f"Field '{field}' is not of a numeric type.")

        # QUESTION: why is this commented out?
        # for field in self.categorical_fields:
        #    if not pd.api.types.is_categorical_dtype(dataframe[field]):
        #        raise ValueError(f"Field '{field}' is not of categorical type.")

        for field in self.textual_fields:
            if not pd.api.types.is_string_dtype(dataframe[field]):
                raise ValueError(f"Field '{field}' is not of a textual type.")

        # QUESTION: why is this commented out?
        # for field in self.imaginal_fields:
        #     if not pd.api.types.is_string_dtype(dataframe[field]):
        #         raise ValueError(f"Field '{field}' is not of a imaginal type.")

        self._validate_time_field(dataframe)


class Labels:
    def __init__(
        self, dataframe: pd.DataFrame, label_field: str, key_field: str, dataset_id: str
    ) -> None:
        self.dataset_id = dataset_id
        if label_field not in dataframe:
            raise Exception(
                "label field doesnt exist in the dataframe, please define an existing column as label_field"
            )
        self.dataframe = dataframe[[label_field, key_field]].copy()
        validate_dataframe_field_names(self.dataframe)
        self.label_field = label_field
        self.key_field = key_field
