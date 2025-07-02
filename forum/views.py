from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TopicForm, PostForm
from .models import Topic, Post


def index(request):
    topics = Topic.objects.order_by('-created_at')
    return render(request, 'forum/index.html', {'topics': topics})


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
            form.save_m2m()
            return redirect('index')
    else:
        form = TopicForm()
    return render(request, 'forum/create_topic.html', {'form': form})


def topic_detail(request, pk):
    topic = Topic.objects.get(pk=pk)
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