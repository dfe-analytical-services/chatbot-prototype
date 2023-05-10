from rest_framework import serializers

class MySerializer(serializers.Serializer):
    question = serializers.CharField()
    sessionId = serializers.CharField()
    documentId = serializers.CharField()