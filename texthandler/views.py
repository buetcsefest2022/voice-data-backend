from cgitb import text
from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
# Create your views here.
from .serializers import TextAudioMapSerializer
from .models import TextAudioMap
from django.db.models import Q

import random

# @api_view(['GET'])
# def getText(request):
#     dataObject = {"text":"hello world"}
#     serializer = TextAudioMapSerializer(data=dataObject)
#     if serializer.is_valid():
#         serializer.save()
#     try:
#         texts = TextAudioMap.objects.all()
#     except TextAudioMap.DoesNotExist:
#         return Response({"error": "error 404"}, status=status.HTTP_404_NOT_FOUND)
#     textSerializer = TextAudioMapSerializer(texts, many=True)
#     return Response({'texts': textSerializer.data}, status=status.HTTP_200_OK)


def collectText():
    texts = TextAudioMap.objects.filter(audio_filename__isnull=True).filter(
        Q(last_accessed__isnull=True) |
        Q(last_accessed__lt=(datetime.now()-timedelta(hours=1)))
    )
    # print(texts[index])

    textSerializer =  TextAudioMapSerializer(texts, many=True)
    index = random.randint(0, len(textSerializer.data)-1)
    # print("random index",index)
    # print(textSerializer.data[index])
    return textSerializer.data[index]


class Text(
    APIView,
    UpdateModelMixin,
    DestroyModelMixin,
):

    def get(self, request):
        # dataObject = {
        #     "text":"with no audio file but accessed",
        #     # "uploaded_by": "jayantasadhu4557@gmail.com",
        #     # "audio_filename": "",
        #     "was_accessed": True,
        #     "last_accessed": datetime.now()
        # }
        # serializer = TextAudioMapSerializer(data=dataObject)
        # if serializer.is_valid():
        #     serializer.save()
        # else:
        #     print('invalid', datetime.now())
        try:
            # texts = TextAudioMap.objects.all()
            textData = collectText()
            return Response({'textData': textData}, status=status.HTTP_200_OK)
        except TextAudioMap.DoesNotExist:
            return Response({"error": "error 404"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, text_id=None, *args, **kwargs):
        try:
            textData = TextAudioMap.objects.get(id=text_id)
            textSerializer = TextAudioMapSerializer(textData, request.data)
            if textSerializer.is_valid():
                textSerializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK )
        except TextAudioMap.DoesNotExist:
            return Response({"error": "error 404"}, status=status.HTTP_404_NOT_FOUND)
        
        
