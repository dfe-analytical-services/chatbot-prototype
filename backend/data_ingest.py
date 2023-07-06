import requests
import json
from bs4 import BeautifulSoup
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm
import tiktoken
from uuid import uuid4
from qdrant_client import QdrantClient
import qdrant_client.models as models
import openai
import os


logging.basicConfig(level = logging.INFO)

# Constants
PUBS_ENDPOINT = "https://content.explore-education-statistics.service.gov.uk/api/publications?page=1&pageSize=9999&sort=published&order=asc"
RELEASE_ENDPOINT = "https://content.explore-education-statistics.service.gov.uk/api/publications/{}/releases/latest"
LINK_ENDPOINT = 'https://explore-education-statistics.service.gov.uk/find-statistics/{}'
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
    dictionary_data = {}
    dictionary_data['url'] = LINK_ENDPOINT.format(slug)
    dictionary_data['data'] = ''
    logging.info(RELEASE_ENDPOINT.format(slug))
    res = requests.get(RELEASE_ENDPOINT.format(slug))
    logging.info(res.status_code)
    text = json.loads(res.text)
    try:
        dictionary_data['data'] += BeautifulSoup(text['headlinesSection']['content'][0]['body'], 'html.parser').get_text()
    except:
        logging.info(f'For {slug} the headlines section doesnt exist')
    for i in range(len(text['content'])):
        try:
            dictionary_data['data'] += BeautifulSoup(text['content'][i]['content'][0]['body'], 'html.parser').get_text()
        except KeyError:
            logging.debug(f"Key does not exist for {slug} at {i}")
    publications_text.append(dictionary_data)
    
logging.info(publications_text)

# Tokenization
tokenizer = tiktoken.get_encoding('p50k_base')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])

chunks = []
for record in publications_text:
    text_temp = text_splitter.split_text(record['data'])
    chunks.extend([{
        'id':str(uuid4()),
        'url': record['url'],
       'text': text_temp[i],
        'chunk':i} for i in range(len(text_temp))])

# Initialize Pinecone
client = QdrantClient("localhost", port = 6333)
collection_names = []
for i in range(len(client.get_collections().collections)):
    collection_names.append(client.get_collections().collections[i].name)
    
if 'ees' in collection_names:
    collection_info = client.get_collection(collection_name = 'ees')
else:
    collection_info = client.create_collection(collection_name = 'ees', vectors_config = models.VectorParams(distance = models.Distance.COSINE,
                                                                                                         size = 1536))

# Process and upload chunks
for i, observation in enumerate(chunks):
    id = i 
    text = observation['text']
    
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        res = openai.Embedding.create(input = text, engine = 'text-embedding-ada-002')
    except Exception as e:
        logging.error(f'The following exception has occured. Could not embed texts: {e}')
        
    client.upsert(collection_name='ees',
                  points = [models.PointStruct(
                      id = i, 
                      payload = {
                          'text': text,
                          'url': observation['url']
                      },
                      vector = res['data'][0]['embedding']
                  )])
    logging.info("Text uploaded")
    
logging.info('Embeddings upserted')
