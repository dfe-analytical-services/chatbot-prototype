from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )
    chunks = []
    for record in text:
        text_temp = text_splitter.split_text(record["text"])
        chunks.extend([{"url": record["link"], "text": text_temp[i]} for i in range(len(text_temp))])

    return chunks
