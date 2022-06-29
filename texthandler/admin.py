from django.contrib import admin
from .models import TextAudioMap
from .models import UserActivity

# Register your models here.
admin.site.register(TextAudioMap)
admin.site.register(UserActivity)