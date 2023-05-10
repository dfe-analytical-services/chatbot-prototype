from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm
from uuid import uuid4
from .utilities import chunking_embed, create_pinecone
import openai
from django.conf import settings


def parse_pdf(document, tokenizer, namespace):
    #document = fitz.open(file)
    whole_text = []
    for index, page in enumerate(document):
        text= page.get_text()
        text = text.replace("\n", ' ')
        text = text.replace("\\xc2\\xa3", "£")
        text = text.replace("\\xe2\\x80\\x93", "-")
        whole_text.append(text)
    
    def tiktoken_len(text):
        tokens = tokenizer.encode(
        text,
        disallowed_special=())
        return len(tokens)
    
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap=100,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""])
    
    chunks = []
    
    for record in tqdm(whole_text):
        texts = text_splitter.split_text(record)
        chunks.extend([{
        'id': str(uuid4()),
        'text': texts[i],
        'chunk': i} for i in range(len(texts))])
    
    index = create_pinecone()
    
    openai.api_key = settings.OPENAI_API_KEY
    
    chunking_embed(batch_size= 100, chunks = chunks, index = index, namespace= namespace)
    
        
    
        
        