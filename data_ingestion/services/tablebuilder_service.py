import logging

import requests

from ..config import settings

logger = logging.getLogger(__name__)


def fetch_data_block(release_id: str, data_block_parent_id: str, key_statistic: dict[str, str]) -> str:
    try:
        response = requests.get(
            url=f"{settings.ees_url_api_data}/tablebuilder/release/{release_id}/data-block/{data_block_parent_id}"
        )
        response.raise_for_status()
        response_json = response.json()
        label = response_json["subjectMeta"]["indicators"][0]["label"]
        measure = list(response_json["results"][0]["measures"].values())[0]
        try:
            unit = response_json["subjectMeta"]["indicators"][0]["unit"]
            measure = f"{measure}{unit}"
        except KeyError:
            logger.error("No unit found")
    except Exception:
        label = key_statistic["title"]
        measure = key_statistic["statistic"]
    try:
        trend = key_statistic["trend"]
        data_string: str = f"{label} - {measure} {trend}."
    except Exception:
        data_string = f"{label} - {measure}."

    return data_string
