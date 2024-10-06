import requests
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Post, Block
from posts.serializers import PostSerializer, BlockSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Post.objects.filter(user_id=self.request.user.id)
    def perform_create(self, serializer):
        post = serializer.save(user_id=self.request.user.id)
        # Send post ID to queue service
        queue_service_url = 'http://queue-service:8000/queue/add/'
        headers = {'Authorization': f'Bearer {self.request.auth}'}
        data = {'post_id': post.id}
        requests.post(queue_service_url, headers=headers, json=data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_id == request.user.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user_id == request.user.id:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = get_object_or_404(Post, pk=request.data['post_id'])
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)