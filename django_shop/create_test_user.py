#!/usr/bin/env python
"""
Создание нового неактивного пользователя для тестирования активации
"""
import os
import django

# Настраиваем Django окружение
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from accounts.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

def create_inactive_user():
    """
    Создаем нового неактивного пользователя для тестирования
    """
    print("🧪 Создание нового неактивного пользователя...")
    
    # Используем уникальный email
    test_email = 'newuser@example.com'
    
    # Удаляем пользователя если он уже существует
    if CustomUser.objects.filter(email=test_email).exists():
        CustomUser.objects.filter(email=test_email).delete()
        print(f"🗑️ Удален существующий пользователь с email {test_email}")
    
    # Создаем нового неактивного пользователя
    user = CustomUser.objects.create_user(
        email=test_email,
        password='TestPassword123!',
        first_name='Новый',
        last_name='Пользователь',
        phone_number='+79009876543',
        is_active=False  # Пользователь неактивен
    )
    
    print(f"✅ Создан пользователь: {user.email}")
    print(f"📋 Активен: {user.is_active}")
    print(f"📧 Email подтверждён: {getattr(user, 'email_confirmed', 'Нет поля')}")
    
    # Генерируем токен активации
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    print(f"🔑 UID: {uid}")
    print(f"🔑 Token: {token}")
    
    # Генерируем ссылку активации
    activation_url = reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
    activation_link = f"http://localhost:8000{activation_url}"
    
    print(f"🔗 Ссылка активации: {activation_link}")
    
    print("\n" + "="*60)
    print("🧪 ТЕСТИРОВАНИЕ АКТИВАЦИИ:")
    print("="*60)
    print("1. Откройте ссылку выше в браузере")
    print("2. Пользователь должен быть активирован")
    print("3. Проверьте статус в админ панели")
    print("="*60)
    
    return user, activation_link

if __name__ == '__main__':
    create_inactive_user()
