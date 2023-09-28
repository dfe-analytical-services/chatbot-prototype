import logging

import requests

from ..config import settings

logger = logging.getLogger(__name__)


def fetch_key_stat(statistic: dict, release_id: str, i: int) -> str:
    try:
        data_block_id = statistic["dataBlockId"]
        res = requests.get(f"{settings.ees_url_api_data}/tablebuilder/release/{release_id}/data-block/{data_block_id}")
        response_json = res.json()
        label = response_json["subjectMeta"]["indicators"][0]["label"]
        measure = list(response_json["results"][0]["measures"].values())[0]
        try:
            unit = response_json["subjectMeta"]["indicators"][0]["unit"]
            measure = f"{measure} {unit}"
        except KeyError:
            logger.error("No unit found")
    except Exception:
        label = statistic["title"]
        measure = statistic["statistic"]
    try:
        trend = statistic["trend"]
        data_string = f"{i + 1}: {label}-{measure} {trend}."
    except Exception:
        data_string = f"{i +1}: {label}-{measure}."

    return data_string
