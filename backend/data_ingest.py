import requests
import json
from bs4 import BeautifulSoup
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm
import tiktoken
from uuid import uuid4
import pinecone
import openai
import os
from time import sleep

import os
import requests
import json
from bs4 import BeautifulSoup
import tiktoken
from uuid import uuid4
import pinecone
import openai
from time import sleep
from tqdm import tqdm

logging.basicConfig(level = logging.INFO)

# Constants
PUBS_ENDPOINT = "https://content.explore-education-statistics.service.gov.uk/api/publications?page=1&pageSize=9999&sort=published&order=asc"
RELEASE_ENDPOINT = "https://content.explore-education-statistics.service.gov.uk/api/publications/{}/releases/latest"
BATCH_SIZE = 100
INDEX_NAME = 'ees'

# Function to make API calls
def fetch_data(endpoint):
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return json.loads(response.text)['results']
    except requests.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
    
# Fetch publication slugs
publications = fetch_data(PUBS_ENDPOINT)
slugs = [publications[i]['slug'] for i in range(len(publications))]
logging.info(slugs)

# Fetch and parse publication content
publications_text = []
for slug in slugs:
    data = ''
    logging.info(RELEASE_ENDPOINT.format(slug))
    res = requests.get(RELEASE_ENDPOINT.format(slug))
    logging.info(res.status_code)
    text = json.loads(res.text)
    try:
        data += BeautifulSoup(text['headlinesSection']['content'][0]['body'], 'html.parser').get_text()
    except:
        logging.info(f'For {slug} the headlines section doesnt exist')
    for i in range(len(text['content'])):
        try:
            data += BeautifulSoup(text['content'][i]['content'][0]['body'], 'html.parser').get_text()
        except KeyError:
            logging.debug(f"Key does not exist for {slug} at {i}")
    publications_text.append(data)
    
logging.info(publications_text)

# Tokenization
tokenizer = tiktoken.get_encoding('p50k_base')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])

chunks = []
for record in tqdm(publications_text):
    text_temp = text_splitter.split_text(record)
    chunks.extend([{
        'id':str(uuid4()),
       'text': text_temp[i],
        'chunk':i} for i in range(len(text_temp))])


# Initialize Pinecone
pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENV'))
print(os.getenv('PINECONE_ENV'))
print(os.getenv('PINECONE_API_KEY'))
index = pinecone.Index(INDEX_NAME)

# Process and upload chunks
for i in tqdm(range(0, len(chunks), BATCH_SIZE)):
    batch_end = min(len(chunks), i + BATCH_SIZE)
    meta_batch = chunks[i:batch_end]
    ids_batch = [x['id'] for x in meta_batch]
    texts = [x['text'] for x in meta_batch]
    embeds = None
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        logging.info(openai.api_key)
        res = openai.Embedding.create(input=texts, engine="text-embedding-ada-002")
    except Exception as e:
            logging.error(f"An error occurred: {e}.")
            break
            
    embeds = [record['embedding'] for record in res['data']]
    meta_batch = [{'text': x['text'], 'chunk': x['chunk']} for x in meta_batch]
    to_upsert = list(zip(ids_batch, embeds, meta_batch))

    # Upsert to Pinecone
    index.upsert(vectors=to_upsert)
    logging.info(f"Embeddings upserted ")
