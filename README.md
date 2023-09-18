# gpt4-langchain-dfe

## Overview

This is a repository for a prototype of a chatbot for the explore-education-statistics service on the government website. The app is powered by embeddings so that when a user inputs a query, the relevant parts of the knowledge base are returned and then the app calls the openai api to answer the question. The tech stack on the backend is the python framework fastapi and the vector database Qdrant.FastApi is a fast, modern framework for building API's in python. For more information about FastApi visit their [documentation](https://fastapi.tiangolo.com/). Langchain is used to query the Qdrant and interact with the openai api. For more information about langchain visit their documentation [here](https://python.langchain.com/en/latest/index.html). For more information on qdrant please visit their documentation here [documentation](https://qdrant.tech/documentation/)
The frontend tech stack is next.js and typescript although this is subject to change

## App structure

There are three projects contained within this repository, a next.js frontend for the project, a fastapi server for the data ingestion, and fastapi server for the project which are in the `chatbot`, `src` and `backend/eesresponseautomater` folders respectively.

The fastapi server for data ingestion has various endpoints to build, rebuild and delete different parts of the vector database, qdrant. To build the database information is extracted from the content apis from the explore-education-statistics service and chunked into smaller units of text. Via the openai and qdrant apis these pieces of text are converted into vector embeddings and subsequently stored in the qdrant vector database. The endpoint to build the database is **.../api/maintenance/publications/build** which is contained in the **src/eessupportbot/routers/maintenance.py** file. This can be used to build or rebuild all the information from the latest publications in the qdrant vector database. There are also endpoints for building information relating to the methodologies and to delete the embeddings stored within the database contained in the same file. The other two files within the router directory, `publications.py` and `methodologies.py` have endpoints for updating a specific publication or methodologies within the qdrant database. For example, if there was a new release of attendance publication, a post request to the **.../pupil-attendance-in-schools/update** could be triggered.


The latter fastapi server exposes the Qdrant, openai and langchain apis which en. This means when a user inputs a question into the app, the question is sent to the **.../api/chat** endpoint. Here the question is converted into a vector embedding. Based on the cosine similarity of this embedding with the embeddings in the vector database, the three most relevant chunks of the vector database are returned. How the api responds is governed by prompt template (contained in `utils.py`) and the `services.message_service.py`. The latter contains a send_message function which encompasses the logic for interacting with th qdrant, openai and langchain apis and allows the endpoint to send a response as an event stream.

## Prequisites

- [Python](https://www.python.org/downloads/) version 3.11 or higher installed on your system.
- [Docker](https://www.docker.com/get-started) installed and running on your system.
- [Pipenv](https://pipenv.pypa.io/en/latest/) for managing Python dependencies.
- [npm](https://nodejs.org/en/download) for managing frontend dependencies. This project uses version 18.16.0



## Development - Initial Setup

1. Clone the repo 
   ```bash
   git clone https://github.com/joesharratt1229/EES_GPT.git
   cd EES_GPT
   ```

2. Install Pipenv if you haven't already:

    ```bash
    pip install pipenv
    ```

3. Create a virtual environment and install project dependencies:

    ```bash
    pipenv install --dev
    ```

4.  Set up pre-commit hooks:

    ```bash
    pipenv run pre-commit install
    ```

5.  In the project's root directory, `.env.example` contains placeholders for environment variables that need to be set. Copy `.env.example` to `.env`:

    ```bash
    cp .env.example .env
    ```

6.  Edit the `.env` file and customise the environment variables.


## Docker Setup

1. Make sure Docker is up and running.

2. To start the project using Docker Compose, run:

    ```bash
    docker-compose up -d
    ```

   This will start the required services defined in `docker-compose.yml`. To stop running the docker container navigate to root of the project directory and run `docker-compose down`

## Running the FastAPI ingestion server
1. To run the FastAPI project locally (outside Docker), make sure you have activated the Pipenv environment:

    ```bash
    pipenv shell
    ```

2. Navigate to the `src` directory:

    ```bash
    cd src
    ```

3. Start the ingestion application:

    ```bash
    uvicorn eessupportbot.main:app --host 0.0.0.0 --port 8000 --reload
    ```

   The API should now be accessible at [http://localhost:8000](http://localhost:8000).

## Upsertion 

To build the database you can send a post request to [http://localhost:8000/api/maintenance/publications/build](http://localhost:8000/api/maintenance/publications/build). If you need help doing this then open up a new bash prompt window and run the following

   ```bash
   chmod +x upsert.sh
   ./upsert.sh
   ```

Once the data is ingested you can stop the FastAPI data ingestion server (if it being run locally)


 ## Usage

- Access the FastAPI backend sever: [http://localhost:8000](http://localhost:8000)
- Access the FastAPI Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Access the Qdrant Docker instance dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

## Web App - initial setup

### FastAPI backend server

Navigate to the root directory of the project in command prompt and run the following.

 ```bash
 pipenv shell
 cd backend/eesresponseautomater
 uvicorn main:app --host 0.0.0.0 --port 8000 --reload
 ```

 The backend server will now be up and running

 ### Next.js frontend
 Navigate to the root directory of the project in command prompt and run the following:
        ```bash
        cd chatbot
        npm install pnpm -g
        pnpm install
        pnpm run dev
        ```
## Usage

- Access the FastAPI backend sever: [http://localhost:8000](http://localhost:8000)
- Access the FastAPI Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Access the Qdrant Docker instance dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)
- Access the Chatbot frontend [http://localhost:3002](http://localhost:3002)
- Access postgres database via pgadmin: [http://localhost:8080](http://localhost:8080)

## Running web App

At this point you should have the environment variables configured, the necessary packages installed to run the fastapi servers and the frontend and a data volume to persist the data stored in qdrant indepedent of shutting down the qdrant container. Each time you want to run the web app open a terminal, navigate to the root of the project and run the following

```bash
docker-compose up -d
pipenv shell
cd backend/eesresponseautomater
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

after this open a terminal and run the following:
```bash
cd chatbot
pnpm run dev
```













