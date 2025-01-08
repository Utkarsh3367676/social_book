from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file_name', 'file_path', 'title', 'description', 'visibility', 'cost', 'year_published', 'uploaded_at']
