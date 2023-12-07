import logging

import requests
from bs4 import BeautifulSoup

from ..config import settings
from ..utils.content_utils import get_content_block_text
from .tablebuilder_service import fetch_data_block

logger = logging.getLogger(__name__)


def extract_releases(slugs: list[str]) -> list[dict[str, str]]:
    return list(map(fetch_release, slugs))


def fetch_release(slug: str) -> dict[str, str]:
    response = requests.get(url=f"{settings.ees_url_api_content}/publications/{slug}/releases/latest")
    response.raise_for_status()
    response_json = response.json()
    release_id = response_json["id"]

    logger.debug(f"Processing content for release id: {release_id}")

    headlines_text = get_headlines_text(res=response_json) or ""
    key_stats_text = get_key_statistics_text(release_id=release_id, res=response_json) or ""
    content_block_text = get_content_block_text(res=response_json)

    return {
        "link": f"{settings.ees_url_public_ui}/find-statistics/{slug}",
        "text": f"{headlines_text}{key_stats_text}{content_block_text}",
    }


def get_headlines_text(res: dict) -> str | None:
    headlines_section = res["headlinesSection"]["content"]
    if headlines_section:
        headlines_content_block = headlines_section[0]
        headlines = BeautifulSoup(markup=headlines_content_block["body"], features="html.parser").get_text()
        return f"Headline: {headlines}"


def get_key_statistics_text(release_id: str, res: dict) -> str | None:
    key_statistics = res["keyStatistics"]
    if key_statistics:
        key_statistics_content = list(
            map(
                lambda item: get_key_statistic_text(release_id=release_id, index_and_key_statistic=item),
                enumerate(key_statistics),
            )
        )
        return "Key statistic ".join(key_statistics_content)


def get_key_statistic_text(release_id: str, index_and_key_statistic: tuple[int, dict[str, str]]) -> str:
    index, key_statistic = index_and_key_statistic
    data_block_id = key_statistic["dataBlockId"]
    return fetch_data_block(
        release_id=release_id, data_block_id=data_block_id, key_statistic=key_statistic, index=index
    )
