# MiniForum

## Introduction

MiniForum — это простой форум на Django с удобным HTML-интерфейсом, позволяющий пользователям регистрироваться, создавать темы и комментарии, ставить лайки и просматривать статистику. Проект предназначен для обучения работе с Django, формами, моделями и аутентификацией.

## Features

- Регистрация, вход и выход пользователей
- Создание, просмотр, редактирование и удаление тем (CRUD)
- Добавление комментариев к темам
- Лайки и просмотры тем
- Аватарки пользователей
- Фильтрация и отображение категорий
- Загрузка изображений для тем
- Навбар с информацией о пользователе и поиском
- Адаптивный дизайн на Bootstrap 4

## Technologies Used

- Python 3.12
- Django 5.2
- Bootstrap 4.5.2
- Pillow
- SQLite
- crispy-forms

## Data Models & Logic

- **User** (встроенная модель Django)
- **Profile** (OneToOneField к User) — хранит аватар пользователя
- **Category** — категории форума
- **Topic** — темы форума  
  - ForeignKey к Category (один-ко-многим)  
  - ForeignKey к User (автор темы)  
  - ManyToManyField к User (лайки)  
- **Post** — комментарии в темах  
  - ForeignKey к Topic (один-ко-многим)  
  - ForeignKey к User (автор комментария)

## Auth System

- Пользователи могут регистрироваться, входить и выходить из системы
- Аватар и имя пользователя отображаются в навбаре
- Авторизованные пользователи могут создавать, редактировать и удалять свои темы и комментарии

## CRUD Functionalities

- Создание, редактирование и удаление тем
- Создание и удаление комментариев к темам
- Лайки тем

## Media & Uploads

- Загрузка изображений для тем через ImageField
- Аватар пользователя с дефолтным изображением, если пользователь не загрузил аватар

## Filtering / Search

- Отображение тем по категориям
- Статистика: число тем, сообщений и пользователей
- Поиск по темам

## Installation & Setup

1. Клонировать репозиторий
  ```
  bash
  git clone <адрес_репозитория>
  cd miniforum
  ```

2. Создать и активировать виртуальное окружение
  ```
  python -m venv venv
  source venv/bin/activate  # Linux/macOS  
  venv\Scripts\activate     # Windows
  ```

3. Установить зависимости
  ```
  pip install -r requirements.txt
  ```


4. Запустить сервер
```
python manage.py runserver
```

## Project Structure
```
miniforum/
├── forum/
│   ├── migrations/
│   ├── templates/forum/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── ...
├── media/
│   ├── avatars/
│   └── topics/
├── static/
├── templates/
│   ├── base.html
│   └── forum/
├── manage.py
└── requirements.txt
```

## Автор

kolokola777
