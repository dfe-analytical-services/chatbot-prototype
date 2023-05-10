from django.db import models
from doc_parse.models import FileUploadMetaData

# Create your models here.
class SessionData(models.Model):
    #id = models.AutoField()
    session_id = models.CharField(max_length=250)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    document_id = models.ForeignKey(FileUploadMetaData, on_delete= models.CASCADE)
