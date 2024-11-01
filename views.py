# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    """View to list all published blog posts."""
    posts = Post.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    """View to display a single blog post with comments."""
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)  # Filter approved comments
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False  # Set to False initially; handle approval logic elsewhere
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[post.slug]))
    else:
        comment_form = CommentForm()  # Create a new comment form if GET request
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def post_create(request):
    """View to create a new blog post."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the logged-in user
            post.save()  # Save the post to the database
            return redirect('post_list')  # Redirect to the list of posts
    else:
        form = PostForm()  # Create a new empty form
    
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, slug):
    """View to edit an existing blog post."""
    post = get_object_or_404(Post, slug=slug)

    # Ensure the user is the author of the post
    if request.user != post.author:
        return redirect('post_detail', slug=slug)  # Redirect to the post detail if not the author
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # Bind the form to the post instance
        if form.is_valid():
            form.save()  # Save the edited post
            return redirect('post_detail', slug=post.slug)  # Redirect to the updated post detail
    else:
        form = PostForm(instance=post)  # Pre-fill the form with the current post data
    
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, slug):
    """View to delete a blog post."""
    post = get_object_or_404(Post, slug=slug)

    # Ensure the user is the author of the post
    if request.user == post.author:
        post.delete()  # Delete the post if the user is the author
        return redirect('post_list')  # Redirect to the list of posts
    
    return redirect('post_detail', slug=slug)  # Redirect to the post detail if not the author