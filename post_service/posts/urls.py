from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, BlockViewSet

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')
router.register(r'blocks', BlockViewSet, basename='block_post')
urlpatterns = router.urls