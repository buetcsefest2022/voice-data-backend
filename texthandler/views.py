from cgitb import text
from datetime import timedelta
from time import sleep
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
# Create your views here.
from .serializers import TextAudioMapSerializer
from .serializers import UserActivitySerializer

from .models import TextAudioMap
from .models import UserActivity
from django.utils import timezone
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

# text_lock_time = 3
# n_tries_limit = 5
# user_blockage_time = 120 # in seconds
# uploads_max_limit = 4

text_lock_time = 1800
n_tries_limit = 30
user_blockage_time = 10*3600 # in seconds
uploads_max_limit = 500

# def addUserUID():
#     global i 
#     if i > 0:
#         return
#     for ids in uids:
#         u = UserActivity(user_uid = ids)
#         u.save()
#     i = i+1
    

@api_view(['POST'])
def addDataTobase(request):
    # print("add command from admin")

    for data in request.data:
        # print(data)
        sleep(0.01)
        try:
            t = TextAudioMap(text = data['text'])
            t.save()
        except:
            print("mara khaisi: ")
            print(data['text'])

    return Response({"success": True}, status=status.HTTP_200_OK )

@api_view(["POST"])
def userUploadsCount(request):
    # print("post here", request.data)
    userEmail = request.data["userEmail"]
    userCount = TextAudioMap.objects.filter(uploaded_by=userEmail).count()
    return Response({"success": True, "upload_count": userCount}, status=status.HTTP_200_OK )


@api_view(["POST"])
def registerUser(request):
    user_uid = request.data["user_uid"]
    if UserActivity.objects.filter(user_uid=user_uid) == 0:
        t = UserActivity(user_uid = user_uid)
        t.save()
        return Response({"success": True}, status=status.HTTP_200_OK )
    else:
        return Response({"success": False}, status=status.HTTP_200_OK )

def chekIfBlocked(user_uid):
    user_activity_data = UserActivity.objects.filter(user_uid=user_uid).values()[0]
    if user_activity_data['n_uploads'] >= uploads_max_limit:
        return True 
    # print(user_activity_data[0])
    # for user in user_activity:
    #     print(user["last_accessed"])
    # is_blocked = user_activity.data['is_blocked']
    if user_activity_data['is_blocked']:
        # check if the time exceeded
        # print("user_blocked")
        if user_activity_data["last_tried"] < (timezone.now() - timedelta(seconds=user_blockage_time)):
            # release the lock 
            UserActivity.objects.filter(id=user_activity_data['id']).update(is_blocked=False, n_tries=0)
            return False 
    else:
        if user_activity_data['n_tries'] >= n_tries_limit:
            # block the user
            UserActivity.objects.filter(id=user_activity_data['id']).update(is_blocked=True)
            return True;
        else:
            return False;

def collectText(user_uid):
    texts = TextAudioMap.objects.filter(audio_filename__isnull=True).filter(
        Q(last_accessed__isnull=True) |
        Q(last_accessed__lt=(timezone.now()-timedelta(seconds=text_lock_time)))
    )

    textSerializer =  TextAudioMapSerializer(texts, many=True)
    if len(textSerializer.data) > 0:
        index = random.randint(0, len(textSerializer.data)-1)
        id = textSerializer.data[index]['id']
        # print("id==", id)
        TextAudioMap.objects.filter(id=id).update(last_accessed=timezone.now())
        # print(textSerializer.data[index])
        user_activity_data = UserActivity.objects.filter(user_uid=user_uid).values()[0]
        UserActivity.objects.filter(id=user_activity_data['id']).update(n_tries=(1+user_activity_data['n_tries']), 
                last_tried=timezone.now())
        return textSerializer.data[index]
    else:
        return {}


class Text(
    APIView,
    UpdateModelMixin,
    DestroyModelMixin,
):

    def post(self, request):
        # dataObject = {
        #     "text":"with no audio file but accessed",
        #     # "uploaded_by": "jayantasadhu4557@gmail.com",
        #     # "audio_filename": "",
        #     "was_accessed": True,
        #     "last_accessed": timezone.now()
        # }
        # serializer = TextAudioMapSerializer(data=dataObject)
        # if serializer.is_valid():
        #     serializer.save()
        # else:
        #     print('invalid', timezone.now())
        try:
            # texts = TextAudioMap.objects.all()
            
            user_uid = request.data["user_uid"]
            # print(user_uid)
            
            if chekIfBlocked(user_uid)==False:
                textData = collectText(user_uid)
                return Response({'textData': textData, "is_blocked": False}, status=status.HTTP_200_OK)
            else:
                return Response({"is_blocked": True}, status=status.HTTP_200_OK)
        except TextAudioMap.DoesNotExist:
            return Response({"error": "error 404"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, text_id=None, *args, **kwargs):
        try:
            # print("Inside put")
            # print(request.data)
            user_activity_data = UserActivity.objects.filter(user_uid=request.data['user_uid']).values()[0]
            textData = TextAudioMap.objects.get(id=text_id)
            textSerializer = TextAudioMapSerializer(textData, request.data)

            if textSerializer.is_valid():
                # print("Valid")
                # print(textSerializer.data)
                textSerializer.save()
                UserActivity.objects.filter(id=user_activity_data['id']).update(n_tries=0, last_upload=timezone.now(),
                n_uploads = (user_activity_data['n_uploads']+1))
            else:
                print(textSerializer.data)
            return Response({"success": True}, status=status.HTTP_200_OK )
        except TextAudioMap.DoesNotExist:
            return Response({"error": "error 404"}, status=status.HTTP_404_NOT_FOUND)
        
        
