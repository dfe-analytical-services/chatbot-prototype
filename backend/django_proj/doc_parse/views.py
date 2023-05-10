from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

import requests

from .serializers import FileUploadSerializers
from .models import FileUploadMetaData
import os


ALLOWED_EXTENSIONS = ['pdf', 'html', 'docx']

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def document_upload(request, *args, **kwargs):
    serializer = FileUploadSerializers(data = request.POST)
    
    endpoint = 'http://localhost:8000/text_extraction/'
    
    if serializer.is_valid():
        uploaded_file_name = serializer.validated_data['file_name']
        type_file = uploaded_file_name.split('.')[-1]
        
        if type_file in ALLOWED_EXTENSIONS:
            matches = FileUploadMetaData.objects.filter(file_name = uploaded_file_name)
            if matches.exists():
                file_uploaded = matches.first()
                response_data = {'file_id': f'namespace_{file_uploaded.id}'}
                return Response(data = response_data, status = status.HTTP_200_OK)
            
            file_uploaded = FileUploadMetaData(file_name = uploaded_file_name, file_size = serializer.validated_data['file_size'],
                                               content_type = serializer.validated_data['content_type'])
            file_uploaded.save()
            uploaded_file = request.FILES['file']
    
            
            with open(f'media/{uploaded_file_name}', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
                    file_path = os.path.join('media', uploaded_file_name)
                    requests.post(endpoint, json = {'destination': file_path ,'file_type': f'{type_file}',
                                                    'file_id': f'namespace_{file_uploaded.id}'}, 
                                  headers={"Content-Type": "application/json"})
                    return Response(data = {'file_id': f'namespace_{file_uploaded.id}'} 
                                    ,status = status.HTTP_201_CREATED)
        else:
            return Response({'Error': 'Unsupported file type'}, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)