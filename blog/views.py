from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment
from .forms import CommentForm, EmailPostForm
from taggit.models import Tag

import json
from django.core.mail import send_mail


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class TagPostListView(ListView):
    model = Tag
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    tag_name = None

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        self.tag_name = tag
        return Post.objects.filter(tags__in=[tag]).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'author', 'content', 'date_posted', 'status', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'author', 'content', 'date_posted', 'status', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def share_post(request, post_id):
    # Get config information for emailing.
    with open('/etc/ajhdotcom_config.json') as config_file:
        config = json.load(config_file)

    # Get the id of the post to share.
    post = get_object_or_404(Post, id=post_id)
    sent = False

    # Process the form when submitted by POST method.
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Send the email...
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['sender']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['sender']}\'s comments: {cd['comments']}"
            send_mail(subject, message, config.get('EMAIL_USER'), [cd['to_email']])
            sent = True
            return render(request, 'blog/share_post.html', {'post': post, 'form': form, 'sent': sent})
    else:
        form = EmailPostForm()
        return render(request, 'blog/share_post.html', {'post': post, 'form': form, 'sent': sent})
