#!/usr/bin/env python
"""
Демонстрационный скрипт для тестирования функциональности системы аутентификации.

Этот скрипт демонстрирует работу с кастомной моделью пользователя
и основными функциями системы регистрации.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from accounts.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def test_user_creation():
    """Тестирует создание пользователей."""
    print("🧪 Тестирование создания пользователей...")
    
    # Создаем обычного пользователя
    user = CustomUser.objects.create_user(
        email='test@example.com',
        password='testpassword123',
        first_name='Тест',
        last_name='Пользователь',
        phone_number='+79991234567',
        address='Москва, ул. Тестовая, д. 1'
    )
    
    print(f"✅ Создан пользователь: {user}")
    print(f"   Email: {user.email}")
    print(f"   Полное имя: {user.get_full_name()}")
    print(f"   Может войти: {user.can_login()}")
    print(f"   Email подтвержден: {user.email_confirmed}")
    
    # Активируем пользователя
    user.is_active = True
    user.email_confirmed = True
    user.save()
    
    print(f"   После активации может войти: {user.can_login()}")
    
    return user


def test_token_generation(user):
    """Тестирует генерацию токенов для активации."""
    print("\n🔑 Тестирование генерации токенов...")
    
    # Генерируем токен активации
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    print(f"✅ Сгенерирован токен для пользователя {user.email}")
    print(f"   UID: {uid}")
    print(f"   Token: {token}")
    
    # Проверяем токен
    is_valid = default_token_generator.check_token(user, token)
    print(f"   Токен действителен: {is_valid}")
    
    return token, uid


def test_user_methods():
    """Тестирует методы модели пользователя."""
    print("\n📋 Тестирование методов пользователя...")
    
    # Создаем пользователя без имени
    user_no_name = CustomUser.objects.create_user(
        email='noname@example.com',
        password='testpassword123'
    )
    
    print(f"✅ Пользователь без имени: {user_no_name}")
    print(f"   Строковое представление: {str(user_no_name)}")
    print(f"   Полное имя: {user_no_name.get_full_name()}")
    print(f"   Короткое имя: {user_no_name.get_short_name()}")
    
    # Создаем пользователя только с именем
    user_first_only = CustomUser.objects.create_user(
        email='firstonly@example.com',
        password='testpassword123',
        first_name='Анна'
    )
    
    print(f"✅ Пользователь только с именем: {user_first_only}")
    print(f"   Строковое представление: {str(user_first_only)}")
    print(f"   Полное имя: {user_first_only.get_full_name()}")
    print(f"   Короткое имя: {user_first_only.get_short_name()}")


def test_user_manager():
    """Тестирует менеджер пользователей."""
    print("\n👑 Тестирование менеджера пользователей...")
    
    try:
        # Пытаемся создать пользователя без email
        CustomUser.objects.create_user(email='', password='test123')
    except ValueError as e:
        print(f"✅ Правильно обработана ошибка: {e}")
    
    # Создаем суперпользователя
    superuser = CustomUser.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword123'
    )
    
    print(f"✅ Создан суперпользователь: {superuser}")
    print(f"   Является суперпользователем: {superuser.is_superuser}")
    print(f"   Является сотрудником: {superuser.is_staff}")
    print(f"   Активен: {superuser.is_active}")


def show_statistics():
    """Показывает статистику пользователей."""
    print("\n📊 Статистика пользователей:")
    
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    confirmed_users = CustomUser.objects.filter(email_confirmed=True).count()
    staff_users = CustomUser.objects.filter(is_staff=True).count()
    
    print(f"   Всего пользователей: {total_users}")
    print(f"   Активных: {active_users}")
    print(f"   С подтвержденным email: {confirmed_users}")
    print(f"   Сотрудников: {staff_users}")
    
    # Показываем всех пользователей
    print(f"\n📝 Список всех пользователей:")
    for user in CustomUser.objects.all():
        status = []
        if user.is_active:
            status.append("активен")
        if user.email_confirmed:
            status.append("email подтвержден")
        if user.is_staff:
            status.append("сотрудник")
        if user.is_superuser:
            status.append("суперпользователь")
        
        status_str = ", ".join(status) if status else "неактивен"
        print(f"   • {user.email} ({user.get_full_name() or 'без имени'}) - {status_str}")


def main():
    """Главная функция демонстрации."""
    print("🚀 Демонстрация системы аутентификации Django\n")
    print("=" * 60)
    
    # Очищаем тестовые данные если они есть
    CustomUser.objects.filter(email__in=[
        'test@example.com',
        'noname@example.com', 
        'firstonly@example.com',
        'admin@example.com'
    ]).delete()
    
    try:
        # Тестируем создание пользователей
        user = test_user_creation()
        
        # Тестируем генерацию токенов
        test_token_generation(user)
        
        # Тестируем методы пользователя
        test_user_methods()
        
        # Тестируем менеджер пользователей
        test_user_manager()
        
        # Показываем статистику
        show_statistics()
        
        print("\n" + "=" * 60)
        print("✅ Все тесты прошли успешно!")
        print("\n🌐 Для проверки веб-интерфейса:")
        print("   1. Запустите сервер: python manage.py runserver")
        print("   2. Откройте браузер: http://127.0.0.1:8000/")
        print("   3. Протестируйте регистрацию и вход")
        print("   4. Проверьте админ-панель: http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении тестов: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Очищаем тестовые данные
        print("\n🧹 Очистка тестовых данных...")
        CustomUser.objects.filter(email__in=[
            'test@example.com',
            'noname@example.com', 
            'firstonly@example.com',
            'admin@example.com'
        ]).delete()
        print("✅ Тестовые данные удалены")


if __name__ == '__main__':
    main()
