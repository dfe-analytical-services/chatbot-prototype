import logging

import qdrant_client.models as models
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import ScoredPoint

from ..config import settings

logger = logging.getLogger(__name__)

client = QdrantClient(location=settings.qdrant_host, port=settings.qdrant_port)


def search(query_vector, limit: int = 5) -> list[ScoredPoint]:
    # Ensure the collection exists - necessary until we have a way of seeding data in Azure
    ensure_collection_exists()

    return client.search(collection_name=settings.qdrant_collection, query_vector=query_vector, limit=limit)


def recreate_collection() -> bool:
    return client.recreate_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=models.VectorParams(distance=models.Distance.COSINE, size=1536),
    )


def ensure_collection_exists() -> None:
    try:
        client.get_collection(collection_name=settings.qdrant_collection)
    except UnexpectedResponse as e:
        if e.status_code == 404:
            logger.debug("Collection doesn't exist - recreating collection")
            recreate_collection()
        else:
            raise
