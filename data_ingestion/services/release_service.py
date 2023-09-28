import logging
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from ..config import settings
from .tablebuilder_service import fetch_key_stat

logger = logging.getLogger(__name__)


def extract_releases(slugs: str) -> List[Dict]:
    texts = []
    for slug in slugs:
        slug_info = {}
        res = requests.get(f"{settings.ees_url_api_content}/publications/{slug}/releases/latest")
        key_stats = {}
        response_json = res.json()
        release_id = response_json["publication"]["releases"][0]["id"]
        try:
            key_statistics = response_json["keyStatistics"]
            if key_statistics != []:
                data_strings = []
                for i, statistic in enumerate(key_statistics):
                    data_strings.append(fetch_key_stat(statistic, release_id, i))
                key_stats["data"] = "Key Statistics section: ".join(data_strings)
        except KeyError:
            logger.warn(f"{slug} doesnt contain key stats")
        try:
            slug_info["text"] = key_stats["data"]
            content = fetch_release(slug, response_json)
            slug_info["text"] += content["data"]
            slug_info["link"] = content["link"]
        except Exception:
            logger.warn(f"{slug} doesnt contain key stats")
            content = fetch_release(slug, response_json)
            slug_info["text"] = content["data"]
            slug_info["link"] = content["link"]
        texts.append(slug_info)
    return texts


def fetch_release(slug: str, res: dict) -> dict:
    slug_content = {}
    slug_content["link"] = f"{settings.ees_url_public_ui}/find-statistics/{slug}"
    try:
        slug_content["data"] = "Headlines Section: "
        slug_content["data"] += BeautifulSoup(res["headlinesSection"]["content"][0]["body"], "html.parser").get_text()
    except Exception as e:
        logger.info(f" Error: {e}. For {slug} the headlines section doesnt exist")

    slug_content["data"] += "Content Section"
    for i in range(len(res["content"])):
        for j in range(len(res["content"][i]["content"])):
            try:
                slug_content["data"] += BeautifulSoup(res["content"][i]["content"][j]["body"], "html.parser").get_text()
            except KeyError:
                logger.debug(f"Key does not exist for {slug} at {i}")
    return slug_content
