"""
URL Configuration for shop_project.

Основная конфигурация URL для проекта интернет-магазина.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Административная панель Django
    path('admin/', admin.site.urls),
    
    # Подключаем URL-ы приложения accounts (регистрация, вход, профиль)
    path('', include('accounts.urls')),
]

# Добавляем обработку медиа файлов для режима разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
