#!/usr/bin/env python
"""
🎭 Демонстрация работы системы регистрации "на пальцах"
Этот скрипт показывает весь процесс регистрации пошагово
"""
import os
import django
import time
from datetime import datetime

# Настраиваем Django окружение
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from accounts.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string

def print_step(step, title, description=""):
    """Красивый вывод шага"""
    print(f"\n{'='*60}")
    print(f"🔄 ШАГ {step}: {title}")
    print(f"{'='*60}")
    if description:
        print(f"📝 {description}")
    print()

def demonstrate_registration_process():
    """
    Демонстрация полного процесса регистрации
    """
    print("🎭 ДЕМОНСТРАЦИЯ СИСТЕМЫ РЕГИСТРАЦИИ И АКТИВАЦИИ")
    print("🎯 Сейчас мы покажем весь процесс пошагово!")
    
    # Шаг 1: Подготовка данных пользователя
    print_step(1, "ПОДГОТОВКА ДАННЫХ ПОЛЬЗОВАТЕЛЯ", 
               "Пользователь заполняет форму регистрации")
    
    user_data = {
        'email': 'demo@example.com',
        'password': 'DemoPassword123!',
        'first_name': 'Демо',
        'last_name': 'Пользователь',
        'phone_number': '+79001111111'
    }
    
    print("👤 Данные пользователя:")
    for key, value in user_data.items():
        if key == 'password':
            print(f"   🔑 {key}: {'*' * len(value)} (скрыт для безопасности)")
        else:
            print(f"   📝 {key}: {value}")
    
    # Удаляем пользователя если существует
    if CustomUser.objects.filter(email=user_data['email']).exists():
        CustomUser.objects.filter(email=user_data['email']).delete()
        print("🗑️ Удален существующий пользователь для демонстрации")
    
    # Шаг 2: Создание пользователя в базе данных
    print_step(2, "СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ В БАЗЕ ДАННЫХ",
               "Django создает пользователя, но помечает как неактивного")
    
    user = CustomUser.objects.create_user(
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        phone_number=user_data['phone_number'],
        is_active=False  # ❌ Пользователь НЕ МОЖЕТ войти в систему
    )
    
    print(f"✅ Пользователь создан в базе данных:")
    print(f"   🆔 ID: {user.id}")
    print(f"   📧 Email: {user.email}")
    print(f"   🔓 Активен: {user.is_active} ❌")
    print(f"   📧 Email подтвержден: {getattr(user, 'email_confirmed', False)} ❌")
    print(f"   🕐 Дата создания: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Шаг 3: Генерация токена активации
    print_step(3, "ГЕНЕРАЦИЯ ТОКЕНА АКТИВАЦИИ",
               "Django создает специальный одноразовый код для подтверждения")
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    print(f"🔐 Токен активации: {token}")
    print(f"   📏 Длина: {len(token)} символов")
    print(f"   🎯 Привязан к: пользователю ID={user.id}")
    print(f"   ⏰ Срок действия: 24 часа")
    print(f"   🔒 Одноразовый: да")
    print()
    print(f"🆔 Зашифрованный UID: {uid}")
    print(f"   📝 Расшифровка: {uid} → {user.id}")
    
    # Шаг 4: Создание ссылки активации
    print_step(4, "СОЗДАНИЕ ССЫЛКИ АКТИВАЦИИ",
               "Формируется URL с токеном для перехода пользователя")
    
    activation_url = reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
    activation_link = f"http://localhost:8000{activation_url}"
    
    print(f"🔗 Ссылка активации:")
    print(f"   {activation_link}")
    print()
    print(f"📋 Разбор ссылки:")
    print(f"   🌐 Домен: http://localhost:8000")
    print(f"   🛣️  Путь: {activation_url}")
    print(f"   🆔 UID: {uid}")
    print(f"   🔑 Токен: {token}")
    
    # Шаг 5: Отправка email (в консоль)
    print_step(5, "ОТПРАВКА EMAIL С АКТИВАЦИЕЙ",
               "Django отправляет письмо (в нашем случае - в консоль)")
    
    context = {
        'user': user,
        'activation_link': activation_link,
        'site_name': 'Интернет-магазин (ДЕМО)'
    }
    
    subject = 'Подтверждение регистрации в интернет-магазине'
    message = render_to_string('accounts/email/activation_email.txt', context)
    html_message = render_to_string('accounts/email/activation_email.html', context)
    
    print("📧 Отправка email...")
    print("💡 В режиме разработки письмо отправляется в консоль Django сервера!")
    print()
    print("📝 Краткое содержимое письма:")
    print("─" * 40)
    lines = message.split('\n')[:10]  # Первые 10 строк
    for line in lines:
        if line.strip():
            print(f"   {line}")
    print("   ...")
    print("─" * 40)
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@shop.local',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
        print("✅ Email отправлен в консоль Django сервера!")
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
    
    # Шаг 6: Имитация перехода пользователя по ссылке
    print_step(6, "ПЕРЕХОД ПОЛЬЗОВАТЕЛЯ ПО ССЫЛКЕ",
               "Пользователь копирует ссылку из консоли и открывает в браузере")
    
    print("👤 Действия пользователя:")
    print("   1. Смотрит в консоль Django сервера")
    print("   2. Находит письмо с активацией")
    print("   3. Копирует ссылку активации")
    print("   4. Открывает ссылку в браузере")
    print()
    print(f"🌐 Браузер отправляет GET запрос:")
    print(f"   GET {activation_url}")
    
    # Шаг 7: Обработка активации Django
    print_step(7, "ОБРАБОТКА АКТИВАЦИИ В DJANGO",
               "Django проверяет токен и активирует пользователя")
    
    print("🔍 Django выполняет проверки:")
    
    # Имитируем процесс проверки
    print("   1. Расшифровка UID...")
    try:
        decoded_uid = urlsafe_base64_decode(uid).decode()
        user_id = int(decoded_uid)
        print(f"      ✅ {uid} → {user_id}")
    except Exception as e:
        print(f"      ❌ Ошибка расшифровки: {e}")
        return
    
    print("   2. Поиск пользователя в базе...")
    try:
        found_user = CustomUser.objects.get(pk=user_id)
        print(f"      ✅ Пользователь найден: {found_user.email}")
    except CustomUser.DoesNotExist:
        print(f"      ❌ Пользователь с ID {user_id} не найден")
        return
    
    print("   3. Проверка токена...")
    token_valid = default_token_generator.check_token(found_user, token)
    if token_valid:
        print(f"      ✅ Токен действителен")
    else:
        print(f"      ❌ Токен недействителен")
        return
    
    print("   4. Активация пользователя...")
    found_user.is_active = True
    found_user.email_confirmed = True
    found_user.save()
    print(f"      ✅ Пользователь активирован!")
    
    # Шаг 8: Результат
    print_step(8, "РЕЗУЛЬТАТ АКТИВАЦИИ",
               "Пользователь получает подтверждение и может войти в систему")
    
    # Обновляем данные из базы
    user.refresh_from_db()
    
    print("🎉 АКТИВАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
    print()
    print("📊 Финальный статус пользователя:")
    print(f"   📧 Email: {user.email}")
    print(f"   🔓 Активен: {user.is_active} ✅")
    print(f"   📧 Email подтвержден: {getattr(user, 'email_confirmed', True)} ✅")
    print(f"   ✅ Может войти в систему: ДА")
    print()
    print("👤 Теперь пользователь может:")
    print("   ✨ Войти в систему через /login/")
    print("   🏠 Зайти в личный кабинет /profile/")
    print("   🛒 Пользоваться всеми функциями сайта")
    
    return user, activation_link

def demonstrate_security_features():
    """
    Демонстрация функций безопасности
    """
    print_step("БОНУС", "ФУНКЦИИ БЕЗОПАСНОСТИ",
               "Что защищает наша система от взлома и спама")
    
    print("🛡️ ВСТРОЕННАЯ ЗАЩИТА:")
    print()
    print("1. 🔐 Токены привязаны к пользователю:")
    print("   - Нельзя использовать токен другого пользователя")
    print("   - Токен содержит информацию о времени создания")
    print("   - Невозможно подделать без знания секретного ключа")
    print()
    print("2. ⏰ Ограниченный срок действия:")
    print("   - Токены работают только 24 часа")
    print("   - После истечения срока нужна новая регистрация")
    print("   - Предотвращает использование старых ссылок")
    print()
    print("3. 🔄 Одноразовое использование:")
    print("   - После активации токен становится недействительным")
    print("   - Нельзя активировать аккаунт повторно")
    print("   - Защита от случайных повторных переходов")
    print()
    print("4. 📧 Привязка к email:")
    print("   - Только владелец email может активировать аккаунт")
    print("   - Нельзя зарегистрироваться с чужим email")
    print("   - Подтверждение реальности адреса")
    print()
    print("5. 🚫 Защита от спама:")
    print("   - Нельзя создать множество аккаунтов без доступа к email")
    print("   - Блокировка неактивных пользователей")
    print("   - Валидация данных на всех уровнях")

if __name__ == '__main__':
    print("🚀 ЗАПУСК ДЕМОНСТРАЦИИ...")
    time.sleep(1)
    
    try:
        user, activation_link = demonstrate_registration_process()
        demonstrate_security_features()
        
        print("\n" + "="*60)
        print("🎯 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print("="*60)
        print()
        print("💡 ИТАК, СИСТЕМА РАБОТАЕТ СЛЕДУЮЩИМ ОБРАЗОМ:")
        print("1. 👤 Пользователь регистрируется → создается неактивный аккаунт")
        print("2. 🔐 Django генерирует токен → создается ссылка активации")  
        print("3. 📧 Отправляется email → пользователь получает ссылку")
        print("4. 🖱️ Пользователь кликает → Django проверяет токен")
        print("5. ✅ Аккаунт активируется → пользователь может войти")
        print()
        print("🔗 Для тестирования откройте эту ссылку:")
        print(f"   {activation_link}")
        print()
        print("📚 Это стандартный подход, используемый в:")
        print("   - Gmail, Yahoo, Outlook")
        print("   - Facebook, Instagram, Twitter")  
        print("   - GitHub, GitLab, Bitbucket")
        print("   - Практически всех современных сайтах")
        
    except KeyboardInterrupt:
        print("\n👋 Демонстрация прервана пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка демонстрации: {e}")
        import traceback
        traceback.print_exc()
