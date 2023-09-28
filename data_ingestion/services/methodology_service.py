import json
import logging

import requests
from bs4 import BeautifulSoup

from ..config import settings
from .vector_db_client import delete_url

logger = logging.getLogger(__name__)


def delete_methodology(slug: str):
    delete_url(url=f"{settings.ees_url_api_content}/methodology{slug}")


def extract_methodologies(slugs):
    texts = []
    for slug in slugs:
        methodology_info = {}
        content = fetch_methodology(slug)
        methodology_info["text"] = content["data"]
        methodology_info["link"] = content["link"]
        texts.append(methodology_info)
    return texts


def fetch_methodology(slug: str):
    methodology_content = {}
    methodology_content["link"] = f"{settings.ees_url_public_ui}/methodology/{slug}"
    res = requests.get(f"{settings.ees_url_api_content}/methodologies/{slug}")
    text = json.loads(res.text)
    try:
        methodology_content["data"] = "Headlines Section: "
        methodology_content["data"] += BeautifulSoup(
            text["headlinesSection"]["content"][0]["body"], "html.parser"
        ).get_text()
    except Exception as e:
        logger.info(f" Error: {e}. For {slug} the headlines section doesnt exist")

    methodology_content["data"] += "Content Section"
    for i in range(len(text["content"])):
        for j in range(len(text["content"][i]["content"])):
            try:
                methodology_content["data"] += BeautifulSoup(
                    text["content"][i]["content"][j]["body"], "html.parser"
                ).get_text()
            except KeyError:
                logger.debug(f"Key does not exist for {slug} at {i}")
    return methodology_content


def fetch_methodology_slugs():
    data = requests.get(f"{settings.ees_url_api_content}/methodology-themes").json()
    slugs = []
    for item in data:
        for topic in item["topics"]:
            for publication in topic["publications"]:
                for methodology in publication["methodologies"]:
                    slugs.append(methodology["slug"])
    return slugs
