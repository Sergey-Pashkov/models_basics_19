"""
ASGI config for shop_project project.

Конфигурация ASGI для проекта shop_project.
"""

import os
from django.core.asgi import get_asgi_application

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')

# Получаем ASGI приложение
application = get_asgi_application()
