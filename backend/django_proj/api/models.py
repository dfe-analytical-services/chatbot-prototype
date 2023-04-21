from django.db import models
import uuid

# Create your models here.
class SessionData(models.Model):
    #id = models.AutoField()
    session_id = models.CharField(max_length=250)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
