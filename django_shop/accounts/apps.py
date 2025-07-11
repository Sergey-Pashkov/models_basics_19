"""
Конфигурация приложения accounts.

Это приложение отвечает за:
- Регистрацию пользователей
- Аутентификацию и авторизацию
- Управление профилями пользователей
- Подтверждение email адресов
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Конфигурация приложения accounts."""
    
    # Тип поля по умолчанию для автоинкрементных первичных ключей
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Имя приложения
    name = 'accounts'
    
    # Человеко-читаемое имя приложения
    verbose_name = 'Управление аккаунтами'
