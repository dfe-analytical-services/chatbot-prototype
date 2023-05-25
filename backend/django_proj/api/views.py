from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import MySerializer
import re
#OpenAI libraries
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
#Custom modules
from .makechain import make_chain, init_pine 
from .models import SessionData

from django.conf import settings


@api_view(['POST'])
def handler(request, *args, **kwargs):
     
    
    serializer = MySerializer(data = request.data)
    
    if serializer.is_valid():
        question = serializer.validated_data['question']
        sessionId = serializer.validated_data['sessionId']
        documentId = serializer.validated_data['documentId']
    else:
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    stripped_question = question.strip().replace('\n', ' ')
    
    try:
        init_pine()
        vector_store = Pinecone.from_existing_index(index_name='edtech-gpt',
                                                    embedding=OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY),
                                                   text_key='text',
                                                   namespace=documentId)
    except Exception as e:
        print('Failed to initialise pinecone', e)
        
    
    chain = make_chain(vector_store)
    
    try:
        result = chain({"question": stripped_question, "chat_history": []})
        #session = SessionData(session_id = sessionId, question = question, answer = result['answer'],
                              #document_id_id = int(re.findall('\d+', documentId)[0]))
        #session.save()
        
        response_data= { 'text': result['answer'], 
                        'sourceDocuments': result['source_documents']}
        return Response(response_data, headers={"Content-Type": "application/json"})
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    
    
