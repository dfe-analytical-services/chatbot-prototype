import fitz
import pinecone
import openai
from tqdm.auto import tqdm
from time import sleep
import os

document = fitz.open('backend/docs/sample.pdf')
pattern = r'(?<=\s)\\.*?\\(?=\s)'

whole_text = []
for index, page in enumerate(document):
    if (index>90 or index < 5):
        continue
    text = page.get_text()
    whole_text.append(text)

decoded_text = {'id':[], 'text':[]}
for ind, page in enumerate(whole_text):
    page = page.replace("\n", ' ')
    page = page.replace("\\xc2\\xa3", "£")
    page = page.replace("\\xe2\\x80\\x93", "-")
    decoded_text['id'].append(str(ind))
    decoded_text['text'].append(page)

pinecone_key = os.environ["PINECONE_API_KEY"]
pinecone.init(api_key=pinecone_key, environment='eu-west1-gcp')

pinecone_ind = pinecone.Index('edtech')

openai.api_key = os.environ["OPENAI_API_KEY"]
embed_model = os.environ["EMBED_MODEL"]

batch_size = 100

for i in tqdm(range(0, len(decoded_text['text']), batch_size)):
    #end the batch
    end_of_batch = min(len(decoded_text['text']), i + batch_size)
    meta_batch = decoded_text['text']
    
    ids_batch = [j for j in decoded_text['id']]
    texts = [x for x in meta_batch][i:end_of_batch]

    try:
        res = openai.Embedding.create(input=texts, engine=embed_model)
    except:
        done = False
        while not done:
            sleep(5)
            try:
                res = openai.Embedding.create(input=texts, engine=embed_model)
                done = True
            except:
                pass
    embedder = [record['embedding'] for record in res['data']]
    
    to_upsert = list(zip(ids_batch, embedder, meta_batch))
    
    pinecone_ind.upsert(vectors=to_upsert)