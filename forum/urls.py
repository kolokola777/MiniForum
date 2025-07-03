from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'), # главная
    path('category/<int:category_id>/', views.category_detail, name='category_detail'), # просмотр тем внутри категории

    path('register/', views.register, name='register'), # регистрация
    path('login/', auth_views.LoginView.as_view(template_name='forum/login.html'), name='login'), # логин
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'), # выход из профиля

    path('create/', views.create_topic, name='create_topic'), # создание темы
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'), # просмотр тем по айди
    path('topic/<int:topic_id>/like/', views.like_topic, name='like_topic'), # лайк
    path('topic/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'), # редактирование тем
    path('topic/<int:topic_id>/delete/', views.delete_topic, name='delete_topic'), # удаление тем

    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'), # редактирование комментариев
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'), # удаление комментариев
]
