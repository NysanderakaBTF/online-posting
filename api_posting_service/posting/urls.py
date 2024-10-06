from django.urls import path
from .views import PostToNetworks
urlpatterns = [
    path('post/', PostToNetworks.as_view()),
]
