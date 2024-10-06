from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConnectedNetworkViewSet
router = DefaultRouter()
router.register(r'', ConnectedNetworkViewSet, basename='connected-network')
urlpatterns = router.urls