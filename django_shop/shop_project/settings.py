"""
Django settings for shop_project project.

Настройки Django для проекта интернет-магазина с системой аутентификации.
"""

from pathlib import Path
import os

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# ВНИМАНИЕ: В продакшене используйте безопасный секретный ключ!
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
# ВНИМАНИЕ: В продакшене отключите режим отладки!
DEBUG = True

ALLOWED_HOSTS = []

# Определение приложений
INSTALLED_APPS = [
    'django.contrib.admin',          # Административная панель Django
    'django.contrib.auth',           # Система аутентификации
    'django.contrib.contenttypes',   # Система типов контента
    'django.contrib.sessions',       # Система сессий
    'django.contrib.messages',       # Система сообщений
    'django.contrib.staticfiles',    # Обработка статических файлов
    'accounts',                      # Наше приложение для работы с пользователями
]

# Промежуточное ПО (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневой файл URL-конфигурации
ROOT_URLCONF = 'shop_project.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Директория для шаблонов
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI приложение
WSGI_APPLICATION = 'shop_project.wsgi.application'

# Настройки базы данных
# Используем SQLite для разработки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Интернационализация
LANGUAGE_CODE = 'ru-ru'  # Русский язык
TIME_ZONE = 'Europe/Moscow'  # Московское время
USE_I18N = True
USE_TZ = True

# Статические файлы (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Медиа файлы (загружаемые пользователями файлы)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Тип поля по умолчанию для автоинкрементных первичных ключей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Указываем нашу кастомную модель пользователя
AUTH_USER_MODEL = 'accounts.CustomUser'

# Настройки email для отправки писем
# В разработке используем консольный бэкенд (письма выводятся в консоль)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@shop.local'

# Для продакшена раскомментируйте и настройте:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'  # Используйте пароль приложения, не основной пароль!

# Пример настройки для Yandex Mail:
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@yandex.ru'
# EMAIL_HOST_PASSWORD = 'your-password'

# Пример настройки для Mail.ru:
# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@mail.ru'
# EMAIL_HOST_PASSWORD = 'your-password'

# URL для перенаправления после успешного входа
LOGIN_REDIRECT_URL = '/profile/'
# URL для перенаправления при выходе
LOGOUT_REDIRECT_URL = '/'
