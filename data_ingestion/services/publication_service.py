import logging

import requests

from ..config import settings
from .vector_db_client import delete_url

logger = logging.getLogger(__name__)


def delete_publication(slug: str) -> None:
    delete_url(url=f"{settings.ees_url_public_ui}/find-statistics/{slug}")


def fetch_publication_slugs() -> list[str]:
    response = requests.get(
        url=f"{settings.ees_url_api_content}/publications?page=1&pageSize=9999&sort=published&order=asc"
    )
    response.raise_for_status()
    response_json = response.json()
    publications = response_json["results"]
    return list(map(lambda publication: publication["slug"], publications))
