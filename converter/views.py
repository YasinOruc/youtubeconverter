from django.shortcuts import render

# converter/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pytube import YouTube
from .models import Download
from .serializers import DownloadSerializer
import os

class YouTubeDownloadView(APIView):
    def post(self, request):
        url = request.data.get('url')
        file_format = request.data.get('format', 'mp4')
        if not url:
            return Response({'error': 'No URL provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Voeg de download toe aan de database
        download = Download.objects.create(url=url, file_format=file_format, status='pending')
        try:
            yt = YouTube(url)
            if file_format == 'mp3':
                stream = yt.streams.filter(only_audio=True).first()
                file_path = stream.download(output_path='downloads/')
                base, ext = os.path.splitext(file_path)
                new_file = base + '.mp3'
                os.rename(file_path, new_file)
            else:
                stream = yt.streams.get_highest_resolution()
                new_file = stream.download(output_path='downloads/')

            # Update status in database
            download.status = 'completed'
            download.save()

            return Response({'message': 'Download successful', 'file_path': new_file}, status=status.HTTP_200_OK)
        except Exception as e:
            download.status = 'failed'
            download.save()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
