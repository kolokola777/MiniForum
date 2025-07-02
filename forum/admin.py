from django.contrib import admin
from .models import Category, Topic, Post, Profile

# Register your models here.

admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Profile)
