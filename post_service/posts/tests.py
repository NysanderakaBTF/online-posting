from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from posts.serializers import PostSerializer


class PostModelTest(TestCase):
    def test_create_post(self):
        post = Post.objects.create(title='Test Post', content='This is a test.', user_id=1)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test.')
        self.assertEqual(post.user_id, 1)
        self.assertEqual(str(post), 'Test Post')

class PostSerializerTest(TestCase):
    def test_serializer_with_valid_data(self):
        data = {'title': 'Test Post', 'content': 'This is a test.'}
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_missing_title(self):
        data = {'content': 'This is a test.'}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


User = get_user_model()

class PostViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'content': 'Content of the new post.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'New Post')

    def test_get_post_list(self):
        Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        Post.objects.create(title='Post 2', content='Content 2', author=self.user)
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_post(self):
        post = Post.objects.create(title='Old Title', content='Old Content', author=self.user)
        url = reverse('post-detail', args=[post.id])
        data = {
            'title': 'Updated Title',
            'content': 'Updated Content'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Title')

    def test_delete_post(self):
        post = Post.objects.create(title='To Delete', content='Content', author=self.user)
        url = reverse('post-detail', args=[post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

