from queue import Queue

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AddPostToQueue(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.user.id
        post_id = request.data.get('post_id')
        queue, _ = Queue.objects.get_or_create(user_id=user_id)
        queue.post_ids.append(post_id)
        queue.save()
        return Response({'status': 'Post added to queue'})

class GetFirstPost(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        queue = Queue.objects.filter(user_id=user_id).first()
        if queue and queue.post_ids:
            return Response({'post_id': queue.post_ids[0]})
        return Response({'post_id': None})

class DeleteFirstPost(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        user_id = request.user.id
        queue = Queue.objects.filter(user_id=user_id).first()
        if queue and queue.post_ids:
            post_id = queue.post_ids.pop(0)
            queue.save()
            return Response({'removed_post_id': post_id})
        return Response({'removed_post_id': None})
