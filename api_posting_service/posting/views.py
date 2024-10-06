from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests

class PostToNetworks(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        headers = {'Authorization': f'Bearer {request.auth}'}
        # Get post from queue service
        queue_url = 'http://queue-service:8000/queue/get_first/'
        queue_response = requests.get(queue_url, headers=headers)
        post_id = queue_response.json().get('post_id')
        if not post_id:
            return Response({'error': 'No post in queue'}, status=404)
        # Format using template service
        format_url = f'http://template-service:8000/templates/format_post/?post_id={post_id}'
        format_response = requests.get(format_url, headers=headers)
        formatted_texts = format_response.json()
        # Simulate posting (since actual posting is not required)
        print(formatted_texts)
        # Remove post from queue
        delete_url = 'http://queue-service:8000/queue/delete_first/'
        requests.delete(delete_url, headers=headers)
        return Response({'formatted_posts': formatted_texts})