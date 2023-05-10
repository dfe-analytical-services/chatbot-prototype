from bs4 import BeautifulSoup
#import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from .utilities import create_pinecone, chunking_embed

from django.conf import settings

def parse_html(file, tokenizer):
    with open(file, 'r') as f:
        html = f.read()
        
    soup = BeautifulSoup(html.text, 'html.parser')
    text = soup.get_text()
    
    text = " ".join(t.strip() for t in soup.stripped_strings)
    decoded_text = text.replace('\xa0', ' ')
    
    #tokenizer = tiktoken.get_encoding('p50k_base')
    
    def tiktoken_len(text):
        tokens = tokenizer.encode(
        text,
        disallowed_special=())
        
        return len(tokens)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap=100, length_function=tiktoken_len, 
                                                   separators=["\n\n", "\n", " ", ""])
    
    chunks = []
    
    texts = text_splitter.split_text(decoded_text)
    chunks.extend([{'id': str(uuid4()), 'text': texts[i],'chunk': i } for i in range(len(texts))])
    
    index = create_pinecone()
    
    chunking_embed(batch_size=100, chunks=chunks, index = index)
    
    
    
    
    
    
    
    
    
    
    