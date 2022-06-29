from dataclasses import field, fields
from importlib.metadata import requires
# from typing_extensions import Required
from rest_framework import serializers
from .models import TextAudioMap
from .models import UserActivity



class TextAudioMapSerializer(serializers.ModelSerializer):
    audio_filename = serializers.CharField(max_length=200, required=False)
    last_accessed = serializers.DateTimeField(required=False)
    text = serializers.CharField(max_length=300,required=False)
    uploaded_by = serializers.CharField(max_length=200,required=False)
    # was_accessed = serializers.BooleanField(default=False)
    audio_url = serializers.URLField(max_length=3000, required=False)

    def create(self, validated_data):
        return TextAudioMap.objects.create(
            audio_filename=validated_data.get('audio_filename'),
            last_accessed=validated_data.get('last_accessed'),
            text=validated_data.get('text'),
            uploaded_by=validated_data.get('uploaded_by'),
            # was_accessed=validated_data.get('was_accessed')
            audio_url=validated_data.get('audio_url')
        )

    def update(self, textAudioMap, validated_data):
        textAudioMap.audio_filename = validated_data.get('audio_filename') if validated_data.get('audio_filename') else textAudioMap.audio_filename
        textAudioMap.last_accessed = validated_data.get('last_accessed') if validated_data.get(
            'last_accessed') else textAudioMap.last_accessed
        textAudioMap.text = validated_data.get('text') if validated_data.get(
            'text') else textAudioMap.text
        textAudioMap.uploaded_by = validated_data.get('uploaded_by') if validated_data.get(
            'uploaded_by') else textAudioMap.uploaded_by
        textAudioMap.audio_url = validated_data.get('audio_url') if validated_data.get('audio_url') else textAudioMap.audio_url
        # textAudioMap.was_accessed = validated_data.get('was_accessed') if validated_data.get('was_accessed') else textAudioMap.was_accessed
        textAudioMap.save()
        return textAudioMap

    class Meta:
        model = TextAudioMap
        fields = (
            'audio_filename',
            'last_accessed',
            'text',
            'uploaded_by',
            'id',
            'audio_url'
        )


class UserActivitySerializer(serializers.ModelSerializer):
    n_tries = serializers.IntegerField(required=False)
    user_uid = serializers.CharField(max_length=200, required=False)
    last_tried = serializers.DateTimeField(required=False)
    last_upload = serializers.DateTimeField(required=False)
    is_blocked = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return TextAudioMap.objects.create(
            n_tries=validated_data.get('n_tries'),
            user_uid=validated_data.get('user_uid'),
            last_tried=validated_data.get('last_tried'),
            last_upload=validated_data.get('last_upload'),
            is_blocked=validated_data.get('is_blocked')
        )

    def update(self, userActivity, validated_data):
        userActivity.n_tries = validated_data.get('n_tries') if validated_data.get('n_tries') else userActivity.n_tries
        userActivity.user_uid = validated_data.get('user_uid') if validated_data.get(
            'user_uid') else userActivity.user_uid
        userActivity.last_tried = validated_data.get('last_tried') if validated_data.get(
            'last_tried') else userActivity.last_tried
        userActivity.last_upload = validated_data.get('last_upload') if validated_data.get(
            'last_upload') else userActivity.last_upload
        userActivity.is_blocked = validated_data.get('is_blocked') if validated_data.get('is_blocked') else userActivity.is_blocked
        userActivity.save()
        return userActivity

    class Meta:
        model = UserActivity
        fields = (
            'last_tried',
            'last_upload',
            'n_tries',
            'is_blocked',
            'id',
            'user_uid'
        )
