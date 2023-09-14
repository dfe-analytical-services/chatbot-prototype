FROM python:3.11

#default values for environment variables
ENV OPENAI_API_MODEL=gpt-4
ENV OPENAI_API_EMBEDDING_MODEL=text-embedding-ada-002
ENV QDRANT_COLLECTION=ees
ENV QDRANT_HOST=localhost
ENV QDRANT_PORT=6333
ENV URL_API_CONTENT=https://content.explore-education-statistics.service.gov.uk/api
ENV URL_PUBLIC_SITE=http://localhost:3002
ENV URL_API_DATA=https://content.explore-education-statistics.service.gov.uk/api

#set working directory
WORKDIR /code

#install required packages
COPY ../requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#copy files
COPY /eesresponseautomater /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]