import logging

import requests
from bs4 import BeautifulSoup

from ..config import settings
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

    headlines_content = str(get_headlines_content(res=response_json))
    key_stats_content = get_key_statistics_content(release_id=release_id, res=response_json)
    general_content = get_general_content(res=response_json)

    return {
        "link": f"{settings.ees_url_public_ui}/find-statistics/{slug}",
        "text": f"{headlines_content}{key_stats_content}{general_content}",
    }


def get_headlines_content(res: dict) -> str | None:
    headlines_section = res["headlinesSection"]["content"]
    if headlines_section:
        headlines_content_block = headlines_section[0]
        headlines = BeautifulSoup(markup=headlines_content_block["body"], features="html.parser").get_text()
        return f"Headline: {headlines}"


def get_key_statistics_content(release_id: str, res: dict) -> str | None:
    key_statistics = res["keyStatistics"]
    if key_statistics:
        key_statistics_content = list(
            map(
                lambda item: get_key_statistic_content(release_id=release_id, index_and_key_statistic=item),
                enumerate(key_statistics),
            )
        )
        return "Key statistic ".join(key_statistics_content)


def get_key_statistic_content(release_id: str, index_and_key_statistic: tuple[int, dict[str, str]]) -> str:
    index, key_statistic = index_and_key_statistic
    data_block_id = key_statistic["dataBlockId"]
    return fetch_data_block(
        release_id=release_id, data_block_id=data_block_id, key_statistic=key_statistic, index=index
    )


def get_general_content(res: dict) -> str:
    content_sections = res["content"]
    result = "Content: "
    for section_index in range(len(content_sections)):
        content_blocks = content_sections[section_index]["content"]
        for block_index in range(len(content_blocks)):
            content_block = content_blocks[block_index]
            if content_block["type"] == "HtmlBlock":
                result += BeautifulSoup(markup=content_block["body"], features="html.parser").get_text()
    return result
