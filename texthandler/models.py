from django.db import models

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

