from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='forum/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('create/', views.create_topic, name='create_topic'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topic/<int:topic_id>/like/', views.like_topic, name='like_topic'),
]
