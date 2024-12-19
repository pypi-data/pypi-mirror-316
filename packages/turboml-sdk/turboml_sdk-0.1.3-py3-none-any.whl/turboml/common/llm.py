from .api import api
from .models import LlamaServerRequest, LlamaServerResponse


def spawn_llm_server(req: LlamaServerRequest) -> LlamaServerResponse:
    res = api.post("model/openai", json=req.model_dump())
    return LlamaServerResponse(**res.json())


def stop_llm_server(server_id: str):
    api.delete(f"model/openai/{server_id}")
