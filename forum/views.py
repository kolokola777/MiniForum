from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TopicForm, PostForm
from .models import Category, Topic, Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


def index(request):
    categories = Category.objects.all()
    stats = {
        'topics': Topic.objects.count(),
        'posts': Post.objects.count(),
        'users': User.objects.count(),
    }

    query = request.GET.get('q', '')
    if query:
        topics = Topic.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        topics = Topic.objects.all().order_by('-created_at')

    return render(request, 'forum/index.html', {
        'categories': categories,
        'stats': stats,
        'topics': topics,
        'query': query,
    })


# Категории
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = category.topic_set.all().order_by('-created_at')
    return render(request, 'forum/category_detail.html', {
        'category': category,
        'topics': topics
    })


# Регистрация
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


# Создание темы
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


# Темы
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


# Лайки для тем
@login_required
def like_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.user in topic.likes.all():
        topic.likes.remove(request.user)
    else:
        topic.likes.add(request.user)
    return redirect('topic_detail', pk=topic.id)


# Изменение темы
@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', pk=topic.id)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'forum/edit_topic.html', {'form': form, 'topic': topic})


# Удаление темы
@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        topic.delete()
        return redirect('index')
    return render(request, 'forum/delete_topic.html', {'topic': topic})


# Изменение комментария
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать чужой комментарий")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', pk=post.topic.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'forum/edit_post.html', {'form': form, 'post': post})


# Удаление комментария
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить чужой комментарий")

    if request.method == 'POST':
        topic_id = post.topic.id
        post.delete()
        return redirect('topic_detail', pk=topic_id)

    return render(request, 'forum/delete_post_confirm.html', {'post': post})
