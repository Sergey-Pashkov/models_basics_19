#!/usr/bin/env python
"""
Скрипт для создания тестового пользователя и проверки отправки email
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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def create_test_user_and_send_email():
    """
    Создаем тестового пользователя и отправляем ему письмо активации
    """
    print("🧪 Создание тестового пользователя...")
    
    # Проверяем, существует ли уже такой пользователь
    test_email = 'testuser@example.com'
    if CustomUser.objects.filter(email=test_email).exists():
        print(f"❌ Пользователь с email {test_email} уже существует!")
        user = CustomUser.objects.get(email=test_email)
        print(f"📋 Существующий пользователь: {user.email}, активен: {user.is_active}")
    else:
        # Создаем нового пользователя
        user = CustomUser.objects.create_user(
            email=test_email,
            password='TestPassword123!',
            first_name='Тестовый',
            last_name='Пользователь',
            phone_number='+79001234567',
            is_active=False  # Пользователь должен активировать аккаунт
        )
        print(f"✅ Создан пользователь: {user.email}")
    
    # Генерируем токен активации
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    print(f"🔑 Токен активации: {token}")
    print(f"🆔 UID: {uid}")
    
    # Формируем ссылку активации
    from django.urls import reverse
    activation_url = reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
    activation_link = f"http://localhost:8000{activation_url}"
    print(f"🔗 Ссылка активации: {activation_link}")
    
    # Подготавливаем содержимое письма
    context = {
        'user': user,
        'activation_link': activation_link,
        'site_name': 'Интернет-магазин'
    }
    
    subject = 'Подтверждение регистрации в интернет-магазине'
    message = render_to_string('accounts/email/activation_email.txt', context)
    html_message = render_to_string('accounts/email/activation_email.html', context)
    
    print("\n" + "="*60)
    print("📧 ОТПРАВКА EMAIL...")
    print("="*60)
    
    try:
        # Отправляем письмо
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@shop.local'),
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
        print("✅ Email отправлен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
    
    print("="*60)
    print("🏁 Тест завершен!")
    
    return user, activation_link

if __name__ == '__main__':
    create_test_user_and_send_email()
