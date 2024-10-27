# converter/models.py
from django.db import models

class Download(models.Model):
    url = models.URLField()
    file_format = models.CharField(max_length=10)  # 'mp3' of 'mp4'
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
