from rest_framework import serializers
from .models import FileUploadMetaData

class FileUploadSerializers(serializers.Serializer):
    file_name = serializers.CharField(max_length = 255)
    file_size = serializers.IntegerField()
    content_type = serializers.CharField(max_length = 100)
    #class Meta:
    #    model = FileUploadMetaData
    #    fields = ('file_name', 'file_size', 'content_type')
        
    
    
    