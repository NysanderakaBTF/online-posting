import re

import requests
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from templatess.models import Template, Block
from templatess.serializers import TemplateSerializer, BlockSerializer
import xml.etree.ElementTree as ET


class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = [IsAuthenticated]

    def get_all_available_blocks(self, request):
        return Block.objects.filter(template__user_id=request.user.id)



class TemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Template.objects.filter(user_id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def format_post(self, request):
        post_id = request.query_params.get('post_id')
        # Get post text from post service
        post_service_url = f'http://post-service:8000/posts/{post_id}/'
        headers = {'Authorization': f'Bearer {request.auth}'}
        post_response = requests.get(post_service_url, headers=headers)
        if post_response.status_code != 200:
            return Response({'error': 'Post not found'}, status=404)
        post = post_response.json()
        # Get connected networks
        networks_url = 'http://connected-networks-service:8000/networks/'
        networks_response = requests.get(networks_url, headers=headers)
        networks = networks_response.json()
        # Get templates
        templates = Template.objects.filter(user_id=request.user.id)
        formatted_texts = []
        for network in networks:
            network_name = network['network_name']
            template = templates.filter(network_name=network_name).first()
            blocks = template.blocks.all(order_by='position')
            formatted_text = ""
            if len(post['blocks']) == 0:
                break
            for block in blocks:
                formatted_text += [i['content'] for i in post['blocks'] if i['name']==block['name']][0]
            formatted_texts.append({'network_name': network_name, 'formatted_text': formatted_text})
        return Response(formatted_texts)
