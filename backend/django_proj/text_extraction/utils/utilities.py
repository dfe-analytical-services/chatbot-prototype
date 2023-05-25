import pinecone
import openai
from time import sleep
from tqdm.auto import tqdm

from django.conf import settings

def create_pinecone():
    
    index_name = 'edtech-gpt'
    
    pinecone.init(
    api_key= settings.PINECONE_API_KEY,
    environment=settings.PINECONE_ENV  )
    
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
        index_name,
        dimension=1536,
        metric='dotproduct')
    
    return pinecone.Index(index_name)


def chunking_embed(chunks, batch_size, index, namespace):
    for i in tqdm(range(0, len(chunks), batch_size)):
        i_end = min(len(chunks), i+batch_size)
        meta_batch = chunks[i:i_end]
        # get ids
        ids_batch = [x['id'] for x in meta_batch]
        # get texts to encode
        texts = [x['text'] for x in meta_batch]
        
        print(len(texts))
        # create embeddings (try-except added to avoid RateLimitError)
        try:
            openai.api_key = settings.OPENAI_API_KEY
            res = openai.Embedding.create(input=texts, engine=settings.OPENAI_API_EMBED_MOD)
        except:
            done = False
            while not done:
                sleep(5)
                try:
                    openai.api_key = settings.OPENAI_API_KEY
                    res = openai.Embedding.create(input=texts, engine=settings.OPENAI_API_EMBED_MOD)
                    done = True
                except:
                    pass
    
        embeds = [record['embedding'] for record in res['data']]
        # cleanup metadata
        meta_batch = [{'text': x['text'], 'chunk': x['chunk']} for x in meta_batch]
    
        to_upsert = list(zip(ids_batch, embeds, meta_batch))
        # upsert to Pinecone
        index.upsert(vectors=to_upsert, namespace = namespace)
        
    return print('Embeddings upserted')