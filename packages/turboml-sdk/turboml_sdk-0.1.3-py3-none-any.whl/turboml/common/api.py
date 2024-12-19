import os
import logging
from typing import Optional
import requests
from .env import CONFIG
import jwt
import time


# Refresh access token if it is about to expire in 1 hour
TOKEN_EXPIRY_THRESHOLD = 3600

logger = logging.getLogger(__name__)


class Api:
    def __init__(self):
        self.session = requests.Session()
        self._api_key: Optional[str] = None
        self._access_token: Optional[str] = None
        self._namespace: Optional[str] = None
        if api_key := os.getenv("TURBOML_API_KEY"):
            self._api_key = api_key
        if namespace := os.getenv("TURBOML_ACTIVE_NAMESPACE"):
            self._namespace = namespace
            logger.debug(
                f"Namespace set to '{namespace}' from environment variable 'TURBOML_ACTIVE_NAMESPACE'"
            )
        else:
            logger.debug(
                "No namespace set; 'TURBOML_ACTIVE_NAMESPACE' environment variable not found."
            )

    def clear_session(self):
        self._api_key = None
        self._access_token = None

    def login(
        self,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        if api_key:
            self._api_key = api_key
            resp = self.session.get(
                url=f"{self.API_BASE_ADDRESS}/user",
                headers=self.headers,
            )
            if resp.status_code != 200:
                self._api_key = None
                raise Exception("Invalid API key")
            return
        if username:
            assert password, "Provide a password along with username"
            resp = self.session.post(
                url=f"{self.API_BASE_ADDRESS}/login",
                data={"username": username, "password": password},
            )
            if resp.status_code != 200:
                raise Exception("Invalid username/password")
            self._access_token = resp.json()["access_token"]
            return
        raise Exception("Provide either an API key or username/password")

    def _refresh_access_token_if_about_to_expire(self) -> None:
        assert self._access_token, "No access token found"
        decoded_jwt = jwt.decode(
            self._access_token,
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        token_expiry = decoded_jwt.get("exp")
        if token_expiry - time.time() < TOKEN_EXPIRY_THRESHOLD:
            resp = self.session.post(
                url=f"{self.API_BASE_ADDRESS}/renew_token",
                headers={"Authorization": f"Bearer {self._access_token}"},
            )
            if resp.status_code != 200:
                raise Exception(
                    "Failed to refresh access token try to login in again using login()"
                )
            self._access_token = resp.json()["access_token"]

    @property
    def API_BASE_ADDRESS(self) -> str:
        return CONFIG.TURBOML_BACKEND_SERVER_ADDRESS + "/api"

    @property
    def headers(self) -> dict[str, str]:
        headers = {}
        if self._namespace:
            headers["X-Turboml-Namespace"] = self._namespace
        if self._api_key:
            headers["Authorization"] = f"apiKey {self._api_key}"
            return headers
        if self._access_token:
            self._refresh_access_token_if_about_to_expire()
            headers["Authorization"] = f"Bearer {self._access_token}"
            return headers
        raise ValueError("No API key or access token found. Please login first")

    def set_active_namespace(self, namespace: str):
        original_namespace = self._namespace
        self._namespace = namespace
        resp = self.get("user/namespace")
        if resp.status_code not in range(200, 300):
            self._namespace = original_namespace
            raise Exception(f"Failed to set namespace: {resp.json()['detail']}")

    @property
    def arrow_headers(self) -> list[tuple[bytes, bytes]]:
        return [(k.lower().encode(), v.encode()) for k, v in self.headers.items()]

    @property
    def namespace(self) -> str:
        return self.get("user/namespace").json()

    def request(
        self,
        method,
        endpoint,
        host=None,
        data=None,
        params=None,
        json=None,
        files=None,
        headers=None,
        exclude_namespace=False,
    ):
        if not host:
            host = self.API_BASE_ADDRESS
        combined_headers = self.headers.copy()
        if headers:
            combined_headers.update(headers)
        # Exclude the namespace header if requested
        if exclude_namespace:
            combined_headers.pop("X-Turboml-Namespace", None)

        resp = self.session.request(
            method=method.upper(),
            url=f"{host}/{endpoint}",
            headers=combined_headers,
            params=params,
            data=data,
            json=json,
            files=files,
        )
        if not (200 <= resp.status_code < 300):
            try:
                json_resp = resp.json()
                error_details = json_resp.get("detail", json_resp)
            except ValueError:
                error_details = resp.text
            raise Exception(
                f"API request failed: {error_details} ({resp.status_code})"
            ) from None
        return resp

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def options(self, endpoint, **kwargs):
        return self.request("OPTIONS", endpoint, **kwargs)

    def head(self, endpoint, **kwargs):
        return self.request("HEAD", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)


api = Api()
