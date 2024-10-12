from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from templatess.models import Template

User = get_user_model()

class TemplateModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='creator@example.com', password='password')

    def test_template_creation(self):
        template = Template.objects.create(
            name='Welcome Template',
            content='Hello, {{ name }}!',
            creator=self.user
        )
        self.assertEqual(template.name, 'Welcome Template')
        self.assertEqual(template.creator, self.user)




class TemplateViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='creator@example.com', password='password')
        self.client.force_authenticate(user=self.user)

    def test_create_template(self):
        url = reverse('template-list')
        data = {
            'name': 'New Template',
            'content': 'Content of the new template.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Template.objects.count(), 1)
        self.assertEqual(Template.objects.get().name, 'New Template')

    def test_get_template_list(self):
        Template.objects.create(name='Template 1', content='Content 1', creator=self.user)
        Template.objects.create(name='Template 2', content='Content 2', creator=self.user)
        url = reverse('template-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
