from django.urls import path
from .views import FolderView

urlpatterns = [
    path('folders/', FolderView.as_view()),
    path('folders/<path:path>/', FolderView.as_view())
]