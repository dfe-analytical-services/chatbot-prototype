# gpt4-langchain-dfe

## Overview

This is a repository for an prototype that allows users to upload pdf, html or word documents and immeditately chat with the document. The tech stack used on the backend is python, django, djagno-rest framework, langchain, pinecone and openai. Langchain is a framework that allows users to build scalalable AI/LLM apps and chatbots. For more information on langchain visit its documentation [here](https://python.langchain.com/en/latest/index.html). Pinecone is a vector store for storing vector embeddings and there are various . The frontend tech stack used is next.js and typescript. I use a django backend. It is important to note that this is just a 
**proof of concepts** to allow the exploration of how something like this would work. The deployed interface is unlikely a chatbot.


## App structure

On the frontend a file upload form is created for users to upload documents which currently supports pdf, html and word document uploads. On the backend an api endpoint in the doc_parse app handles a file upload. This application serves two functions: firstly it sends a document identifier to the frontend which is stored in the client's session storage which is used to redirect the client and converse with the specific document. It also sends a post request to the text extraction api endpoint. This endpoint converts the text into vector embeddings. These embeddings are split into chunks and upserted to the vector database, pinecone. 

Once redirected to the chat url the client sends the question as a post request to the api endpoint. The 4 most numerically similary chunks to the question are retrieved which are then fed in as context to the Chat GPT 4 api which sends the response a long with the source documents to the client. 


## Development

1. Clone the repo 
```
git clone [azure devops url]
```

2. Make sure python and pip are installed. Navigate to the project directory and change the directory to `backend`. From here it is necessary to create and activate a virtual environment to install python dependencids.

```
cd backend

python -m venv env

\env\scripts\activate.bat

pip install -r requirements.txt
```

3. After installation change the directory to django_proj and create a `.env` file with the api keys of the strcutre outlined below. You will need to sign up to [openai](https://platform.openai.com) and pinecone and then generate api keys [pinecone](https://app.pinecone.io/) :

```
PINECONE_ENV = "YOUR PINECONE ENV"
PINECONE_API_KEY = "YOUR API KEY"
OPENAI_API_KEY= "YOUR OPEN API KEY"
OPENAI_API_EMBED_MOD = "text-embedding-ada-002"
MODEL = "gpt-3-turbo" or whatever model you have access to
```

#### NOTE if you do not have access to gpt4 you will need to change the model to gpt3.5-turbo in the `api.makechain.py` folder in the django project

4. To run the backend navigate to the root of the django project and run the following:
``` 
python manage.py runserver 8000
```

5. On the frontend navigate to the `chatbot` directory of the project. Once you have installed node.js run `npm install pnpm -g`. This installs pnpm globally. Then run `pnpm install`

6. To run the frontend you then run `pnpm run dev`. 








