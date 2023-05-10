from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import os
from django.conf import settings
import tiktoken
import fitz
import openai

from .serializers import EmbeddingExtractionSerializer
from .utils.pdf_parse import parse_pdf
from .utils.html_parse import parse_html

# Create your views here.

@api_view(['POST'])
def store_embeddings(request, *args, **kwargs):
    serializer = EmbeddingExtractionSerializer(data = request.data)
    print(request.data)
    if serializer.is_valid():
        destination = serializer.validated_data['destination']
        file_type = serializer.validated_data['file_type']
        namespace = serializer.validated_data['file_id']
        #return  Response(status = status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    path = os.path.join(settings.BASE_DIR, destination) 
    document = fitz.open(path)
    openai.api_key = settings.OPENAI_API_KEY
    
    tokenizer = tiktoken.get_encoding('p50k_base')
    
    if file_type == 'pdf':
        parse_pdf(document=document, tokenizer=tokenizer, namespace= namespace)
    else:
        parse_html(document = document, tokenizer=tokenizer)
    
    return Response(status = status.HTTP_200_OK)
        