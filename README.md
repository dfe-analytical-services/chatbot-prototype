# gpt4-langchain-dfe

## Overview

This is a repository for a prototype of a chatbot for the explore-education-statistics service on the government website. The app is powered by embeddings so that when a user inputs a query, the relevant parts of the knowledge base are returned and then the app calls the openai api to answer the question. The tech stack on the backend is the python framework fastapi and the vector database Qdrant.FastApi is a fast, modern framework for building API's in python. For more information about FastApi visit their [documentation](https://fastapi.tiangolo.com/). Langchain is used to query the Qdrant and interact with the openai api. For more information about langchain visit their documentation [here](https://python.langchain.com/en/latest/index.html). The frontend tech stack is next.js and typescript although this is subject to change

## App structure

A user's question is sent as a post request to the backend and if it is validated is converted into a vector embedding. Based on the cosine similarity of this embedding with the embeddings in the vector database, the six more relevant chunks of the vector database are returned and then the openai api is used  to answer a user's question about the EES service. How the api responds is governed by the prompt template in **utils.py** on the backend. This prompt template can be used to mitigate the risk of the the ai hallucinating and also governs how the ai responds if the question is not related to the service. 

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

3. After installation change the directory to `fastapi` and create a `.env` file with the api keys of the strcutre outlined below. You will need to sign up to [openai](https://platform.openai.com). :

```
OPENAI_API_KEY= "YOUR OPEN API KEY"
```

#### NOTE if you do not have access to gpt4 you will need to change the model to gpt3.5-turbo in the `utils.py` folder in the fastapi folder

4. To run the backend navigate to the root of the django project and run the following:
``` 
python -m uvicorn main::app --reload
``` 
5. Open another command prompt window and navigate to the `chatbot` directory of the project. Once you have installed node.js run `npm install pnpm -g`. This installs pnpm globally. Then run `pnpm install`

6. To run the frontend you then run `pnpm run dev`. 








