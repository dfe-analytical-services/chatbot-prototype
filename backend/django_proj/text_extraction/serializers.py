from rest_framework import serializers

class EmbeddingExtractionSerializer(serializers.Serializer):
    destination = serializers.CharField(max_length = 250)
    file_type = serializers.CharField(max_length = 100)
    file_id = serializers.CharField()