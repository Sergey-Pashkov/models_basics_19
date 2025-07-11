#!/usr/bin/env python
"""
Проверка статуса активации пользователя
"""
import os
import django

# Настраиваем Django окружение
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from accounts.models import CustomUser

def check_user_status():
    """
    Проверяем статус пользователей
    """
    print("👥 СТАТУС ПОЛЬЗОВАТЕЛЕЙ:")
    print("=" * 50)
    
    for user in CustomUser.objects.all():
        print(f"📧 {user.email}")
        print(f"   ✅ Активен: {user.is_active}")
        print(f"   📧 Email подтверждён: {getattr(user, 'email_confirmed', 'Нет поля')}")
        print(f"   🕐 Создан: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
        print(f"   👤 Администратор: {user.is_staff}")
        print("-" * 40)

if __name__ == '__main__':
    check_user_status()
