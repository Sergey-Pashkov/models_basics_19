"""
WSGI config for shop_project project.

Конфигурация WSGI для проекта shop_project.
"""

import os
from django.core.wsgi import get_wsgi_application

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')

# Получаем WSGI приложение
application = get_wsgi_application()
