#!/usr/bin/env python
"""
Тестовый скрипт для проверки отправки email в Django проекте
"""
import os
import django

# Настраиваем Django окружение
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def test_email_sending():
    """
    Тестируем отправку email через Django
    """
    print("🔧 Тестирование отправки email...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Не задан')}")
    print("-" * 50)
    
    # Тест 1: Простое письмо
    print("📧 Тест 1: Отправка простого письма")
    try:
        send_mail(
            subject='Тестовое письмо Django',
            message='Это простое тестовое письмо из Django.',
            from_email='test@shop.local',
            recipient_list=['test@example.com'],
            fail_silently=False
        )
        print("✅ Простое письмо отправлено успешно!")
    except Exception as e:
        print(f"❌ Ошибка отправки простого письма: {e}")
    
    print("-" * 50)
    
    # Тест 2: Письмо с HTML шаблоном
    print("📧 Тест 2: Отправка письма с HTML шаблоном")
    try:
        # Подготавливаем контекст
        context = {
            'user': {'first_name': 'Тестовый', 'email': 'test@example.com'},
            'activation_link': 'http://localhost:8000/accounts/activate/test-token/',
            'site_name': 'Интернет-магазин'
        }
        
        # Рендерим шаблоны
        text_message = render_to_string('accounts/email/activation_email.txt', context)
        html_message = render_to_string('accounts/email/activation_email.html', context)
        
        print("📝 Содержимое текстового письма:")
        print(text_message)
        print("-" * 30)
        
        # Отправляем письмо
        send_mail(
            subject='Подтверждение регистрации (тест)',
            message=text_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@shop.local'),
            recipient_list=['test@example.com'],
            html_message=html_message,
            fail_silently=False
        )
        print("✅ Письмо с шаблоном отправлено успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка отправки письма с шаблоном: {e}")
    
    print("-" * 50)
    print("🏁 Тестирование завершено!")

if __name__ == '__main__':
    test_email_sending()
