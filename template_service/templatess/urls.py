from django.urls import path
from rest_framework.routers import DefaultRouter

from templatess.views import BlockViewSet, TemplateViewSet

router = DefaultRouter()


router.register(r'', TemplateViewSet, basename='template')
router.register(r'blocks', BlockViewSet, basename='block')
urlpatterns = router.urls

urlpatterns += [
    path('blocks/all_user_blocks', BlockViewSet.as_view({'get': 'get_all_available_blocks'}))
]
