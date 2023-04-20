#Rest framework libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import MySerializer
#OpenAI libraries
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
import pinecone
#Custom modules
from .makechain import make_chain, init_pine 



@api_view(['POST'])
def handler(request, *args, **kwargs):
    serializer = MySerializer(data = request.data)
    
    if serializer.is_valid():
        question = serializer.validated_data['question']
        print(question)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    stripped_question = question.strip().replace('\n', ' ')
    
    try:
        init_pine()
        vector_store = Pinecone.from_existing_index(index_name='edtech-gpt',
                                                    embedding=OpenAIEmbeddings(openai_api_key=""),
                                                   text_key='text')
    except Exception as e:
        print('Failed to initialise pinecone', e)
        
    
    chain = make_chain(vector_store)
    try:
        result = chain({"question": stripped_question, "chat_history": []})
        response_data= { 'text': result['answer'], 
                        'sourceDocuments': result['source_documents'],
                        'brian': 59}
        return Response(response_data, headers={"Content-Type": "application/json"})
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    
    
