import logging

import requests
from bs4 import BeautifulSoup

from ..config import settings
from ..utils.content_utils import get_content
from .tablebuilder_service import fetch_data_block

logger = logging.getLogger(__name__)


def extract_releases(slugs: list[str]) -> list[dict[str, str]]:
    return list(map(fetch_release, slugs))


def fetch_release(slug: str) -> dict[str, str]:
    response = requests.get(url=f"{settings.ees_url_api_content}/publications/{slug}/releases/latest")
    response.raise_for_status()
    response_json = response.json()
    release_id = response_json["id"]

    logger.debug(f"Processing content for publication: {slug}, latest release id: {release_id}")

    headlines_text = get_headlines_text(res=response_json) or ""
    key_stats_text = get_key_statistics_text(release_id=release_id, res=response_json) or ""
    content_block_text = get_content(content_sections=response_json["content"])
    all_text = f"{headlines_text}{key_stats_text}{content_block_text}"

    return {
        "link": f"{settings.ees_url_public_ui}/find-statistics/{slug}",
        "text": all_text,
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
        results = []
        for count, item in enumerate(key_statistics, start=1):
            type = item["type"]
            if type == "KeyStatisticDataBlock":
                data_block_parent_id = item["dataBlockParentId"]
                result = fetch_data_block(
                    release_id=release_id, data_block_parent_id=data_block_parent_id, key_statistic=item
                )
                results.append(f"Key statistic {count}: {result}")
            elif type == "KeyStatisticText":
                results.append(f"Key statistic {count}: {item['title']} - {item['statistic']} - {item['trend']}.")
            else:
                raise ValueError(f"Unknown key statistic type: {type}")

        return " ".join(results)
