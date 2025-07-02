from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# Профиль пользователя (аватар, биография)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Профиль {self.user.username}'


# Категория тем (например: Общение, Новости)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Темы на форуме
class Topic(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='topics/', blank=True, null=True)
    favorites = models.ManyToManyField(User, related_name='favorite_topics', blank=True)

    def __str__(self):
        return self.title


# Сообщения внутри темы
class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} → {self.topic.title}'


