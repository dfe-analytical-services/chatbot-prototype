import logging
import time
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from adrf.decorators import api_view
from rest_framework import status
from .serializers import MySerializer
#OpenAI libraries
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
#Custom modules
from .makechain import make_chain 

from django.conf import settings

logger = logging.getLogger(__name__)

@api_view(['POST'])
async def handler(request, *args, **kwargs):
    start_time = time.time()
    serializer = MySerializer(data = request.data)
    
    if serializer.is_valid():
        question = serializer.validated_data['question']
    else:
        logger.error("Validation Error: question is not a string")
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    stripped_question = question.strip().replace('\n', ' ')
    
    try:
        vector_store = Pinecone.from_existing_index(index_name='ees',
                                                    embedding=OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY),
                                                   text_key='text')
    except TypeError as error:
        logger.error('Vector store failed to initialise:', error)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    similar_docs = vector_store.similarity_search(query = stripped_question, k = 4)
    
    chain = make_chain()
    
    async def async_generate(chain, inputs = input, q = question):
        resp = await chain.arun(input_documents = inputs, question = q)
        return resp
    
    try:
        result = await async_generate(chain, similar_docs, stripped_question)
        
        response_data= { 'text': result}
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.debug("Time taken to process the request: %s seconds", elapsed_time)
        return Response(response_data, headers={"Content-Type": "application/json"})
    except Exception as e:
        logger.error("Failed with error %s", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
 
    
    
    
    
    
