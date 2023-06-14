import logging
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
from .langchainprompt import QA_PROMPT

from django.conf import settings

logger = logging.getLogger(__name__)

@api_view(['POST'])
async def handler(request, *args, **kwargs):
    serializer = MySerializer(data = request.data)
    logger.debug(request.data)
    
    if serializer.is_valid():
        question = serializer.validated_data['question']
    else:
        logger.error("Invalid request")
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    stripped_question = question.strip().replace('\n', ' ')
    
    vector_store = Pinecone.from_existing_index(index_name='edtech-gpt',
                                                    embedding=OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY),
                                                   text_key='text')
                                                   #namespace=documentId)   
    
    similar_docs = vector_store.similarity_search(query = stripped_question, int = 4)
    logger.debug(similar_docs)
    
    chain = make_chain()
    
    async def async_generate(chain, inputs = input, question = question):
        resp = await chain.arun(input_documents = inputs, question = question)
        return resp
    
    try:
        result = await async_generate(chain, similar_docs, stripped_question)
        
        response_data= { 'text': result}
        logger.debug("Response data: %s", response_data)
        return Response(response_data, headers={"Content-Type": "application/json"})
    except Exception as e:
        logger.error("Failed with error %s", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
 
    
    
    
    
    
