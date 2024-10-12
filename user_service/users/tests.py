from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)




class RegistrationTestCase(APITestCase):
    def test_registration(self):
        url = reverse('rest_register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_registration_password_mismatch(self):
        url = reverse('rest_register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password321'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', response.data)


