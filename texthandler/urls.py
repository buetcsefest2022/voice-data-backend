from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.Text.as_view()),
    path('<int:text_id>/',views.Text.as_view()),
    path('adminDataUpload/', views.addDataTobase),
    path("upCount/", views.userUploadsCount),
]
