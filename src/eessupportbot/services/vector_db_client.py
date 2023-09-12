import logging

import openai
import qdrant_client.models as models
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

from ..config import settings
from ..utils import chunk_text

logger = logging.getLogger(__name__)

client = QdrantClient(settings.qdrant_host, port=settings.qdrant_port)


def data_upsertion(slugs, func, batch_size=100) -> None:
    get_collection()
    text = func(slugs)
    chunks = chunk_text(text)
    for i in range(0, len(chunks), batch_size):
        end_index = min(i + batch_size, len(chunks))
        batch_meta = chunks[i:end_index]
        batch_text = [chunks[j]["text"] for j in range(i, end_index)]
        try:
            embeds = openai.Embedding.create(input=batch_text, engine=settings.embedding_model)
        except Exception as e:
            logger.error(f"An error occured within embedding model: {e}")

        formatted_embeddings = [embeds["data"][j]["embedding"] for j in range(len(embeds["data"]))]
        client.upsert(
            collection_name=settings.qdrant_collection,
            points=models.Batch(
                ids=[j for j in range(i, end_index)],
                payloads=batch_meta,
                vectors=formatted_embeddings,
            ),
        )

        logger.info("Batch upserted")

    logger.info("Text upserted")


def recreate_collection():
    return client.recreate_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=models.VectorParams(distance=models.Distance.COSINE, size=1536),
    )


def get_collection():
    try:
        client.get_collection(collection_name=settings.qdrant_collection)
    except UnexpectedResponse:
        logger.debug("EES database doesn't exist - need to create database")
        recreate_collection()


def delete_url(url: str):
    client.delete(
        collection_name=settings.qdrant_collection,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="url",
                        match=models.MatchValue(value=url),
                    ),
                ]
            ),
        ),
    )
