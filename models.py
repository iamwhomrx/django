# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    """Model representing a category for blog posts."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    """Model representing a blog post."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']  # Order posts by published date, newest first

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a particular post."""
        from django.urls import reverse
        return reverse('post_detail', args=[self.slug])

class Comment(models.Model):
    """Model representing a comment on a blog post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']  # Order comments by creation date, newest first

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'
