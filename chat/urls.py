from django.urls import path
from .views import predict_emotion

urlpatterns = [path('predict/', predict_emotion)]
