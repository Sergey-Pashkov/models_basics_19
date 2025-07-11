#!/usr/bin/env python
"""
Отладка URL активации
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

def debug_activation_urls():
    """
    Отладка генерации URL активации
    """
    print("🔍 ОТЛАДКА URL АКТИВАЦИИ")
    print("=" * 50)
    
    # Получаем тестового пользователя
    try:
        user = CustomUser.objects.get(email='testuser@example.com')
        print(f"✅ Найден пользователь: {user.email}")
    except CustomUser.DoesNotExist:
        print("❌ Тестовый пользователь не найден")
        return
    
    # Генерируем новый токен
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    print(f"🔑 UID: {uid}")
    print(f"🔑 Token: {token}")
    
    # Генерируем URL через reverse
    try:
        activation_url = reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
        print(f"🔗 Relative URL: {activation_url}")
        
        # Полный URL
        full_url = f"http://localhost:8000{activation_url}"
        print(f"🌐 Full URL: {full_url}")
        
    except Exception as e:
        print(f"❌ Ошибка генерации URL: {e}")
    
    # Проверим также прямую генерацию
    direct_url = f"/activate/{uid}/{token}/"
    print(f"📍 Direct URL: {direct_url}")
    
    print("\n🧪 ТЕСТОВЫЕ URL для проверки:")
    print(f"✅ http://localhost:8000{activation_url}")
    print(f"✅ http://localhost:8000{direct_url}")
    
    # Проверим настройки URL
    print("\n📋 URL PATTERNS:")
    from accounts.urls import urlpatterns
    for pattern in urlpatterns:
        if hasattr(pattern, 'name') and pattern.name == 'activate':
            print(f"🎯 Found activate pattern: {pattern.pattern}")

if __name__ == '__main__':
    debug_activation_urls()
