from django.db import models

# Create your models here.
class FileUploadMetaData(models.Model):
    file_name = models.TextField(max_length=250)
    file_size = models.IntegerField()
    content_type = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    