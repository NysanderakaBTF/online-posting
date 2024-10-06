from django.urls import path
from .views import AddPostToQueue, GetFirstPost, DeleteFirstPost
urlpatterns = [
    path('add/', AddPostToQueue.as_view()),
    path('get_first/', GetFirstPost.as_view()),
    path('delete_first/', DeleteFirstPost.as_view()),
]