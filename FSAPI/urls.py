from django.urls import path
from .views.folder import FolderView
from .views.topic import TopicView
from .views.topiclist import TopicListView

urlpatterns = [
    path('folders/', FolderView.as_view()),
    path('folders/<path:path>/', FolderView.as_view()),
    path('topics/', TopicListView.as_view()),
    path('topics/<int:pk>/', TopicView.as_view()),
]