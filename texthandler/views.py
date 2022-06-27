from cgitb import text
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
# Create your views here.
from .serializers import TextAudioMapSerializer
from .models import TextAudioMap


@api_view(['GET'])
def getText(request):
    dataObject = {"audio_filename":"hello world"}
    serializer = TextAudioMapSerializer(data=dataObject)
    if serializer.is_valid():
        serializer.save()
    try:
        texts = TextAudioMap.objects.all()
    except TextAudioMap.DoesNotExist:
        return Response({"error": "error 404"}, status=status.HTTP_404_NOT_FOUND)
    textSerializer = TextAudioMapSerializer(texts, many=True)
    return Response({'texts': textSerializer.data}, status=status.HTTP_200_OK)
