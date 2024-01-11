import logging

from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint

from ..config import settings

logger = logging.getLogger(__name__)

client = QdrantClient(location=settings.qdrant_host, port=settings.qdrant_port)


def search(query_vector, limit: int = 5) -> list[ScoredPoint]:
    return client.search(collection_name=settings.qdrant_collection, query_vector=query_vector, limit=limit)
