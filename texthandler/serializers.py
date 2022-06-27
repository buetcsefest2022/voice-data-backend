from dataclasses import field, fields
from importlib.metadata import requires
# from typing_extensions import Required
from rest_framework import serializers
from .models import TextAudioMap



class TextAudioMapSerializer(serializers.ModelSerializer):
    audio_filename = serializers.CharField(max_length=200, required=False)
    last_accessed = serializers.DateField(required=False)
    text = serializers.CharField(max_length=300,required=False)
    uploaded_by = serializers.CharField(max_length=200,required=False)
    was_accessed = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return TextAudioMap.objects.create(
            audio_filename=validated_data.get('audio_filename'),
            last_accessed=validated_data.get('last_accessed'),
            text=validated_data.get('text'),
            uploaded_by=validated_data.get('uploaded_by'),
            was_accessed=validated_data.get('was_accessed')
        )

    def update(self, textAudioMap, validated_data):
        textAudioMap.audio_filename = validated_data.get('audio_filename') if validated_data.get('audio_filename') else textAudioMap.audio_filename
        textAudioMap.last_accessed = validated_data.get('last_accessed') if validated_data.get(
            'last_accessed') else textAudioMap.last_accessed
        textAudioMap.text = validated_data.get('text') if validated_data.get(
            'text') else textAudioMap.text
        textAudioMap.uploaded_by = validated_data.get('uploaded_by') if validated_data.get(
            'uploaded_by') else textAudioMap.uploaded_by
        textAudioMap.was_accessed = validated_data.get('was_accessed') if validated_data.get('was_accessed') else textAudioMap.was_accessed
        textAudioMap.save()
        return textAudioMap

    class Meta:
        model = TextAudioMap
        fields = (
            'audio_filename',
            'last_accessed',
            'text',
            'uploaded_by',
            'was_accessed',
            'id'
        )
