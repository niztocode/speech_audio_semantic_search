from __future__ import annotations

import logging
import os

import weaviate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)
logger = logging.getLogger(__name__)


class Settings:
    def __init__(self: Settings) -> None:
        self.weaviate_http_host: str = os.environ["WEAVIATE_HTTP_HOST"]
        self.weaviate_http_port: int = int(os.environ["WEAVIATE_HTTP_PORT"])
        self.weaviate_grpc_host: str = os.environ["WEAVIATE_GRPC_HOST"]
        self.weaviate_grpc_port: int = int(os.environ["WEAVIATE_GRPC_PORT"])
        # self.weaviate_api_key: str = os.environ["WEAVIATE_API_KEY"]


config = Settings()


def get_weaviate_client() -> weaviate.WeaviateClient:
    logger.info(
        "Created client to Weaviate DB @ %s:%s",
        config.weaviate_http_host,
        config.weaviate_http_port,
    )
    return weaviate.connect_to_local()


w_client = get_weaviate_client()
