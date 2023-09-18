import json
import logging

import requests

from ..config import settings
from .vector_db_client import delete_url

logger = logging.getLogger(__name__)


def delete_publication(slug: str):
    delete_url(url=f"{settings.url_public_site}/find-statistics/{slug}")


def fetch_publication_slugs():
    try:
        response = requests.get(
            f"{settings.url_api_content}/publications?page=1&pageSize=9999&sort=published&order=asc"
        )
        response.raise_for_status()
        publications = json.loads(response.text)["results"]
        slugs = [publications[i]["slug"] for i in range(len(publications))]
        return slugs
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
