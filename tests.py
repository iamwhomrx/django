# blog/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Category, Post, Comment
from django.contrib.auth.models import User

class CategoryModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Django', slug='django')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Django')

class PostModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Django', slug='django')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), reverse('post_detail', args=[self.post.slug]))

class CommentModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Django', slug='django')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name='Test Commenter',
            email='commenter@example.com',
            content='This is a test comment.'
        )

    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'Comment by Test Commenter on Test Post')

class PostViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Django', slug='django')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test post.')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'blog/post_list.html')