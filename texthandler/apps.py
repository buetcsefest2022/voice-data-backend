from django.apps import AppConfig


class TexthandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'texthandler'

class UserActivityHandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userActivityHandler'
