import logging

import openai
from openai import OpenAIError

from ..config import settings

logger = logging.getLogger(__name__)

openai.api_key = settings.openai_api_key


def get_embeddings(question: str):
    try:
        return openai.Embedding.create(input=question, engine=settings.openai_embedding_model)
    except OpenAIError as openai_exception:
        logger.exception(openai_exception, exc_info=True)
        raise


def get_embedding(question: str):
    embeddings = get_embeddings(question)

    return embeddings.data[0].embedding
