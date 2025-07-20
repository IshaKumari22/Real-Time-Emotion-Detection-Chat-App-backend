from django.urls import path
from .views import ThreadListCreateView, MessageListCreateView

urlpatterns = [
    path('threads/', ThreadListCreateView.as_view(), name='threads'),
    path('threads/<int:thread_id>/messages/', MessageListCreateView.as_view(), name='thread-messages'),
]
