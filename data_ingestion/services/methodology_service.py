import logging

import requests

from ..config import settings
from ..utils.content_utils import get_content_block_text
from .vector_db_client import delete_url

logger = logging.getLogger(__name__)


def delete_methodology(slug: str) -> None:
    delete_url(url=f"{settings.ees_url_api_content}/methodology{slug}")


def extract_methodologies(slugs: list[str]) -> list[dict[str, str]]:
    return list(map(fetch_methodology, slugs))


def fetch_methodology(slug: str) -> dict[str, str]:
    try:
        response = requests.get(url=f"{settings.ees_url_api_content}/methodologies/{slug}")
        response.raise_for_status()
        response_json = response.json()
        methodology_version_id = response_json["id"]

        logger.debug(f"Processing content for methodology version: {methodology_version_id}")

        return {
            "link": f"{settings.ees_url_public_ui}/methodology/{slug}",
            "text": get_content_block_text(res=response_json),
        }
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            logger.error(f"Methodology version for slug {slug} was not found")
            return {}
        else:
            raise


def fetch_methodology_slugs() -> list[str]:
    response = requests.get(url=f"{settings.ees_url_api_content}/methodology-themes")
    response.raise_for_status()
    response_json = response.json()
    slugs: list[str] = []
    for item in response_json:
        for topic in item["topics"]:
            for publication in topic["publications"]:
                for methodology in publication["methodologies"]:
                    slugs.append(methodology["slug"])
    return slugs
