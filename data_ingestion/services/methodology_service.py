import logging

import requests

from ..config import settings
from ..utils.content_utils import get_content
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

        logger.debug(f"Processing content for methodology: {slug}, methodology version id: {methodology_version_id}")

        content_block_text = get_content(content_sections=response_json["content"])
        annexes_block_text = get_content(content_sections=response_json["annexes"])
        all_text = content_block_text + (" " + annexes_block_text if content_block_text else annexes_block_text)

        return {
            "link": f"{settings.ees_url_public_ui}/methodology/{slug}",
            "text": all_text,
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
