# EES chatbot prototype

## Overview

This is a repository for a prototype of a chatbot for the Department for Education (DfE) [Explore Education Statistics](https://explore-education-statistics.service.gov.uk/) service.

The app is powered by embeddings so that when a user inputs a query, the relevant parts of the knowledge base are returned and then the app calls the openai api to answer the question.

The tech stack on the backend is the python framework fastapi and the vector database Qdrant.FastApi is a fast, modern framework for building APIs in python. For more information about FastApi visit their [documentation](https://fastapi.tiangolo.com/). Langchain is used to query the Qdrant and interact with the openai api. For more information about langchain visit their [documentation](https://python.langchain.com/en/latest/index.html). For more information on qdrant please visit their [documentation](https://qdrant.tech/documentation/).

The frontend tech stack is next.js and typescript although this is subject to change.

## App structure

There are three projects contained within this repository, a next.js frontend UI project, a fastapi server for the data ingestion, and fastapi server for the backend which are in the `chatbot-ui`, `data_ingestion` and `response_automater` folders respectively.

The fastapi server for data ingestion has various endpoints to build, rebuild and delete different parts of the vector database, qdrant. To build the database information is extracted from the content apis from the explore-education-statistics service and chunked into smaller units of text. Via the openai and qdrant apis these pieces of text are converted into vector embeddings and subsequently stored in the qdrant vector database. The endpoint to build the database is **.../api/maintenance/publications/build** which is contained in the **data_ingestion/routers/maintenance.py** file. This can be used to build or rebuild all the information from the latest publications in the qdrant vector database. There are also endpoints for building information relating to the methodologies and to delete the embeddings stored within the database contained in the same file. The other two files within the router directory, `publications.py` and `methodologies.py` have endpoints for updating a specific publication or methodologies within the qdrant database. For example, if there was a new release of attendance publication, a post request to the **.../pupil-attendance-in-schools/update** could be triggered.


The latter fastapi server exposes the Qdrant, openai and langchain apis which en. This means when a user inputs a question into the app, the question is sent to the **.../api/chat** endpoint. Here the question is converted into a vector embedding. Based on the cosine similarity of this embedding with the embeddings in the vector database, the three most relevant chunks of the vector database are returned. How the api responds is governed by prompt template (contained in `utils.py`) and the `services.message_service.py`. The latter contains a send_message function which encompasses the logic for interacting with the qdrant, openai and langchain apis and allows the endpoint to send a response as an event stream.

## Prerequisites

- [Python](https://www.python.org/downloads/) version 3.11 or higher installed on your system.
- [Docker](https://www.docker.com/get-started) installed and running on your system.
- [Pipenv](https://pipenv.pypa.io/en/latest/) for managing Python dependencies.
- [npm](https://nodejs.org/en/download) for managing frontend dependencies.



## Development - Initial Setup

1. Clone the repo
   ```bash
   git clone https://github.com/joesharratt1229/EES_GPT.git
   cd EES_GPT
   ```

2. Install [pnpm](https://pnpm.io) if you haven't already:

    ```bash
    npm install -g pnpm
    ```

3. Install [Pipenv](https://pipenv.pypa.io/en/latest/) if you haven't already:

    ```bash
    pip install pipenv
    ```

4. Create a virtual environment and install project dependencies:

    ```bash
    pipenv install --dev
    ```

5.  Set up pre-commit hooks:

    ```bash
    pipenv run pre-commit install
    ```

6.  In the project's root directory, `.env.example` contains placeholders for environment variables that need to be set. Copy `.env.example` to `.env`:

    ```bash
    cp .env.example .env
    ```

7.  Edit the `.env` file and customise the environment variables.


## Docker Setup

1. Make sure Docker is up and running.

2. To start the project using Docker Compose, run:

    ```bash
    docker-compose up -d
    ```

   This will start the required services defined in `docker-compose.yml`. To stop running the docker container navigate to root of the project directory and run `docker-compose down`

## Qdrant

Qdrant is the vector database running locally using Docker.

Access the Qdrant Docker instance dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

## Running the FastAPI data ingestion server

1. To run the project locally (outside Docker), make sure you have activated the Pipenv environment:

    ```bash
    pipenv shell
    ```

2. Start the data ingestion server:

    ```bash
    uvicorn data_ingestion.main:app --host 0.0.0.0 --port 8000 --reload
    ```

3. Access the data ingestion API docs: [http://localhost:8000/docs](http://localhost:8000/docs).

 ### Ingesting data

The python script `scripts/data_ingest.py` can be used as a helper to make API requests for data maintenance.

Once the data is ingested you can stop the FastAPI data ingestion server (if it's being run locally).

You can run the script with the help of `pnpm` using `pnpm data-ingest`.

For help:

   ```bash
   pnpm data-ingest --help
   ```

To clear the vector database:

   ```bash
   pnpm data-ingest --clear
   ```

To build all methodologies:

   ```bash
   pnpm data-ingest --build-methodologies
   ```

To build all publications:

   ```bash
   pnpm data-ingest --build-publications
   ```

To update a specific methodology:

   ```bash
   pnpm data-ingest --update-methodology --slug SLUG
   ```

To update a specific publication:

   ```bash
   pnpm data-ingest --update-publication --slug SLUG
   ```

## Running the FastAPI response automater server

1. To run the project locally (outside Docker), make sure you have activated the Pipenv environment:

    ```bash
    pipenv shell
    ```

2. Start the response automater server.

    ```bash
    uvicorn response_automater.main:app --host 0.0.0.0 --port 8010 --reload
    ```

3. Access the response automater API docs: [http://localhost:8010/docs](http://localhost:8010/docs).
 
 ## Running the Next.js Chatbot UI frontend

1. Install all dependencies for the project:

    ```bash
    pnpm i
    ```

2. Start Next.js:

    ```bash
    pnpm --filter chatbot-ui dev
    ```
3. Access the chatbot UI: [http://localhost:3002](http://localhost:3002).

## Quick start

This is a guide to starting up the chatbot UI assuming you have already followed the initial setup and run everything once before.

It assumes you have already run the data ingestion server at least once so that you now have a Qdrant data volume and you have used the API to ingest data.

1. Open a new command prompt in the root directory of the project and run the following:

    ```bash
    docker-compose up -d
    pipenv shell
    uvicorn response_automater.main:app --host 0.0.0.0 --port 8000 --reload
    ```

2. Open a new command prompt in the root directory of the project and run the following:

    ```bash
    pnpm --filter chatbot-ui dev
    ```
