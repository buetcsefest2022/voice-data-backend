from django.db import models
from django.forms import IntegerField

# Create your models here.


class TextAudioMap(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    audio_filename = models.CharField(
        max_length=200,
        default=None,
        blank=True,
        null=True
    )

    last_accessed = models.DateTimeField(
        default=None,
        null=True
    )

    text = models.CharField(
        max_length=300,
        default=None,
        blank=False,
        null=True
    )
    uploaded_by = models.CharField(
        max_length=200,
        default=None,
        blank=True,
        null=True
    )
    # was_accessed = models.BooleanField(
    #     default=None
    # )
    audio_url = models.URLField(
        default=None,
        max_length = 3000,
        blank=True,
        null=True
    )

class UserActivity(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    last_tried = models.DateTimeField(
        default=None,
        null=True,
    )

    last_upload = models.DateTimeField(
        default= None,
        null=True
    )

    n_tries = models.IntegerField(
        default = 0,
        null=False 
    )

    is_blocked = models.BooleanField(
        default=False,
        null=True 
    )

    user_uid = models.CharField (
        max_length=200,
        default=None,
        blank=False,
        null=False 
    )

    n_uploads = models.IntegerField(
        default=0,
        null=True
    )
