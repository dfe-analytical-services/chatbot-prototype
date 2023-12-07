from bs4 import BeautifulSoup


def get_content_block_text(res: dict) -> str:
    content_sections = res["content"]
    result = "Content: "
    for section_index in range(len(content_sections)):
        content_blocks = content_sections[section_index]["content"]
        for block_index in range(len(content_blocks)):
            content_block = content_blocks[block_index]
            if content_block["type"] == "HtmlBlock":
                result += BeautifulSoup(markup=content_block["body"], features="html.parser").get_text()
    return result
