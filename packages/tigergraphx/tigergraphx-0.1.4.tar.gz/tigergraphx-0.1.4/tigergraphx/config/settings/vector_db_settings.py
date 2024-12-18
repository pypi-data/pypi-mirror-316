from typing import Optional
from pathlib import Path
from lancedb import timedelta, ThreadPoolExecutor

from ..base_config import BaseConfig


class BaseVectorDBConfig(BaseConfig):
    """Base configuration class for vector databases."""

    type: str  # Mandatory type field to identify the database type.


class LanceDBConfig(BaseVectorDBConfig):
    """Configuration class for LanceDB."""

    type: str = "LanceDB"  # Default type for LanceDBConfig.
    table_name: str = (
        "entity_description_embeddings"  # Default table name for embeddings.
    )
    uri: str | Path  # URI or path to the LanceDB resource.
    api_key: Optional[str] = None  # API key for authentication, if required.
    region: str = "us-east-1"  # Default region for LanceDB.
    host_override: Optional[str] = None  # Host override for custom LanceDB endpoints.
    read_consistency_interval: Optional[timedelta] = (
        None  # Read consistency interval for queries.
    )
    request_thread_pool: Optional[int | ThreadPoolExecutor] = (
        None  # Thread pool for requests.
    )


class NanoVectorDBConfig(BaseVectorDBConfig):
    """Configuration class for NanoVectorDB."""

    type: str = "NanoVectorDB"  # Default type for NanoVectorDBConfig.
    storage_file: str | Path = "nano-vectordb.json"  # Path to the storage file.
    embedding_dim: int = 1536  # Default embedding dimension.
