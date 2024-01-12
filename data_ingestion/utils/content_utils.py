import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_content(content_sections: list[dict]) -> str:
    content_section_texts = list(filter(None, map(get_content_section_text, content_sections)))
    if not content_section_texts:
        return ""
    return " ".join(content_section_texts)


def get_content_section_text(content_section) -> str | None:
    if content_section.get("content") is not None:
        content_blocks = content_section["content"]
        content_block_texts = list(filter(None, map(get_content_block_text, content_blocks)))
        if len(content_block_texts) > 0:
            section_heading = content_section["heading"]
            return f"{section_heading}: " + " ".join(content_block_texts)


def get_content_block_text(content_block) -> str | None:
    if content_block["type"] == "HtmlBlock":
        if content_block.get("body") is not None:
            return BeautifulSoup(markup=content_block["body"], features="html.parser").get_text()
