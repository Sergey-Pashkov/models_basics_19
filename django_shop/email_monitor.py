#!/usr/bin/env python
"""
Email Monitoring Tool для Django проекта
Отслеживает все отправляемые email в реальном времени
"""

import os
import sys
import time
from datetime import datetime

def monitor_emails():
    """
    Мониторинг email в режиме реального времени
    """
    print("="*70)
    print("📧 EMAIL MONITORING TOOL для Django интернет-магазина")
    print("="*70)
    print(f"🕐 Запуск мониторинга: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    print("📋 ИНСТРУКЦИИ:")
    print("1. Запустите Django сервер: python manage.py runserver")
    print("2. Перейдите на http://localhost:8000/accounts/register/")
    print("3. Зарегистрируйте нового пользователя")
    print("4. Наблюдайте за email в этом окне!")
    print("")
    print("⚠️  НАСТРОЙКИ EMAIL:")
    print("   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'")
    print("   Все email будут выводиться в консоль Django сервера")
    print("")
    print("🔍 Если email не отображаются, проверьте:")
    print("   ✓ Запущен ли Django сервер")
    print("   ✓ Правильные ли настройки EMAIL_BACKEND в settings.py")
    print("   ✓ Нет ли ошибок в views.py при отправке email")
    print("")
    print("="*70)
    print("📧 ТЕСТИРОВАНИЕ EMAIL СИСТЕМЫ:")
    print("="*70)
    
    # Показываем примеры команд для тестирования
    django_dir = "/Users/macbook/Яндекс.Диск/Visual Studio/models_basics_19/django_shop"
    
    print(f"\n🧪 Для тестирования выполните в другом терминале:")
    print(f"cd {django_dir}")
    print("python test_email.py          # Простой тест email")
    print("python test_user_email.py     # Тест с созданием пользователя")
    print("python manage.py runserver    # Запуск Django сервера")
    print("")
    
    print("🌐 URL для тестирования в браузере:")
    print("http://localhost:8000/accounts/register/     # Регистрация")
    print("http://localhost:8000/accounts/login/        # Вход")
    print("http://localhost:8000/accounts/profile/      # Профиль")
    print("")
    
    print("📊 СТАТИСТИКА EMAIL:")
    print("="*70)
    
    # Проверяем, можем ли мы подключиться к Django
    try:
        # Настраиваем Django окружение
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
        import django
        django.setup()
        
        from django.conf import settings
        from accounts.models import CustomUser
        
        print(f"✅ Django подключен успешно!")
        print(f"📧 EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        print(f"📬 DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Не задан')}")
        
        # Статистика пользователей
        total_users = CustomUser.objects.count()
        active_users = CustomUser.objects.filter(is_active=True).count()
        inactive_users = CustomUser.objects.filter(is_active=False).count()
        
        print(f"👥 Всего пользователей: {total_users}")
        print(f"✅ Активных пользователей: {active_users}")  
        print(f"⏳ Неактивных пользователей: {inactive_users}")
        
        if inactive_users > 0:
            print(f"\n📩 Пользователи ожидающие активации:")
            for user in CustomUser.objects.filter(is_active=False)[:5]:
                print(f"   • {user.email} (создан: {user.date_joined.strftime('%Y-%m-%d %H:%M')})")
                
    except Exception as e:
        print(f"❌ Ошибка подключения к Django: {e}")
    
    print("\n" + "="*70)
    print("🚀 ГОТОВ К МОНИТОРИНГУ EMAIL!")
    print("="*70)
    print("💡 Совет: Держите это окно открытым во время тестирования")
    print("📧 Все email будут отображаться в консоли Django сервера")
    print("\nДля выхода нажмите Ctrl+C")
    
    try:
        while True:
            time.sleep(10)
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Мониторинг активен...")
    except KeyboardInterrupt:
        print("\n👋 Мониторинг завершен!")

if __name__ == '__main__':
    # Переходим в директорию Django проекта
    django_dir = "/Users/macbook/Яндекс.Диск/Visual Studio/models_basics_19/django_shop"
    if os.path.exists(django_dir):
        os.chdir(django_dir)
    
    monitor_emails()
