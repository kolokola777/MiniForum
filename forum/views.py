from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TopicForm, PostForm
from .models import Category, Topic, Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


def index(request):
    categories = Category.objects.all()
    stats = {
        'topics': Topic.objects.count(),
        'posts': Post.objects.count(),
        'users': User.objects.count(),
    }
    return render(request, 'forum/index.html', {
        'categories': categories,
        'stats': stats
    })


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = category.topic_set.all().order_by('-created_at')
    return render(request, 'forum/category_detail.html', {
        'category': category,
        'topics': topics
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'forum/register.html', {'form': form})


@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('index')
    else:
        form = TopicForm()
    return render(request, 'forum/create_topic.html', {'form': form})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    topic.views += 1
    topic.save(update_fields=['views'])

    posts = Post.objects.filter(topic=topic).order_by('created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.topic = topic
                post.author = request.user
                post.save()
                return redirect('topic_detail', pk=pk)
        else:
            return redirect('login')
    else:
        form = PostForm()

    return render(request, 'forum/topic_detail.html', {
        'topic': topic,
        'posts': posts,
        'form': form
    })


@login_required
def like_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.user in topic.likes.all():
        topic.likes.remove(request.user)
    else:
        topic.likes.add(request.user)
    return redirect('topic_detail', pk=topic.id)
