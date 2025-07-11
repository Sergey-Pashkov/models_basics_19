"""
Представления (views) для приложения accounts.

Содержит логику обработки запросов для:
- Регистрации и активации пользователей
- Входа и выхода из системы
- Управления профилем
- Восстановления пароля
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from .models import CustomUser
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    UserProfileForm,
    CustomPasswordChangeForm,
    PasswordResetRequestForm,
    AccountDeletionForm
)


def home(request):
    """
    Главная страница сайта.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Отрендеренная главная страница
    """
    return render(request, 'accounts/home.html')


@csrf_protect
@never_cache
def register(request):
    """
    Страница регистрации пользователя.
    
    Обрабатывает регистрацию нового пользователя и отправляет
    письмо с подтверждением email адреса.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Форма регистрации или перенаправление
    """
    # Если пользователь уже авторизован, перенаправляем на профиль
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя (пока неактивного)
            user = form.save()
            
            # Генерируем токен для подтверждения email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Создаем ссылку активации
            activation_link = request.build_absolute_uri(
                reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Подготавливаем содержимое письма
            subject = 'Подтверждение регистрации в интернет-магазине'
            message = render_to_string('accounts/email/activation_email.txt', {
                'user': user,
                'activation_link': activation_link,
                'site_name': 'Интернет-магазин'
            })
            html_message = render_to_string('accounts/email/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
                'site_name': 'Интернет-магазин'
            })
            
            try:
                # Отправляем письмо с подтверждением
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@shop.local',
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False
                )
                
                messages.success(
                    request,
                    f'Регистрация прошла успешно! На адрес {user.email} отправлено письмо '
                    'с инструкциями по активации аккаунта.'
                )
                
                return redirect('accounts:email_confirmation_sent')
                
            except Exception as e:
                # В случае ошибки отправки письма
                messages.error(
                    request,
                    'Произошла ошибка при отправке письма подтверждения. '
                    'Попробуйте зарегистрироваться позже или обратитесь к администратору.'
                )
                # Удаляем созданного пользователя, так как письмо не отправилось
                user.delete()
        else:
            messages.error(
                request,
                'Пожалуйста, исправьте ошибки в форме регистрации.'
            )
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'title': 'Регистрация'
    })


def activate(request, uidb64, token):
    """
    Активация аккаунта пользователя по токену.
    
    Проверяет токен активации и активирует аккаунт пользователя,
    если токен действительный.
    
    Args:
        request: HTTP запрос
        uidb64: Закодированный ID пользователя
        token: Токен активации
        
    Returns:
        HttpResponse: Страница результата активации
    """
    try:
        # Декодируем ID пользователя
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Токен действительный, активируем пользователя
        user.is_active = True
        user.email_confirmed = True
        user.save()
        
        messages.success(
            request,
            'Ваш аккаунт успешно активирован! Теперь вы можете войти в систему.'
        )
        
        return render(request, 'accounts/activation_success.html', {
            'user': user,
            'title': 'Аккаунт активирован'
        })
    else:
        # Токен недействительный или пользователь не найден
        messages.error(
            request,
            'Ссылка активации недействительна или срок её действия истёк. '
            'Попробуйте зарегистрироваться заново.'
        )
        
        return render(request, 'accounts/activation_invalid.html', {
            'title': 'Ошибка активации'
        })


def email_confirmation_sent(request):
    """
    Страница уведомления об отправке письма подтверждения.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Страница уведомления
    """
    return render(request, 'accounts/email_confirmation_sent.html')


@csrf_protect
@never_cache
def user_login(request):
    """
    Страница входа в систему.
    
    Обрабатывает аутентификацию пользователя с дополнительными
    проверками безопасности.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Форма входа или перенаправление
    """
    # Если пользователь уже авторизован, перенаправляем на профиль
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Записываем IP адрес последнего входа
            user.last_login_ip = get_client_ip(request)
            user.save(update_fields=['last_login_ip'])
            
            # Входим в систему
            login(request, user)
            
            # Проверяем, нужно ли запомнить пользователя
            remember_me = form.cleaned_data.get('remember_me')
            if remember_me:
                # Устанавливаем время жизни сессии на 30 дней
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 дней в секундах
            else:
                # Сессия истечет при закрытии браузера
                request.session.set_expiry(0)
            
            messages.success(
                request,
                f'Добро пожаловать, {user.get_short_name()}!'
            )
            
            # Перенаправляем пользователя туда, откуда он пришел, или на профиль
            next_url = request.GET.get('next', 'accounts:profile')
            return redirect(next_url)
        else:
            messages.error(
                request,
                'Пожалуйста, исправьте ошибки в форме входа.'
            )
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'title': 'Вход в систему'
    })


def get_client_ip(request):
    """
    Получение IP адреса клиента.
    
    Args:
        request: HTTP запрос
        
    Returns:
        str: IP адрес клиента
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def user_logout(request):
    """
    Выход из системы.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Перенаправление на главную страницу
    """
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('accounts:home')


@login_required
def profile(request):
    """
    Личный кабинет пользователя.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Страница профиля пользователя
    """
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    """
    Редактирование профиля пользователя.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Форма редактирования профиля
    """
    # Временная заглушка - будем развивать на следующем шаге
    return render(request, 'accounts/edit_profile.html')


@login_required
def change_password(request):
    """
    Изменение пароля пользователя.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Форма изменения пароля
    """
    # Временная заглушка - будем развивать на следующем шаге
    return render(request, 'accounts/change_password.html')


@login_required
def delete_account(request):
    """
    Удаление аккаунта пользователя.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Форма подтверждения удаления
    """
    # Временная заглушка - будем развивать на следующем шаге
    return render(request, 'accounts/delete_account.html')


def password_reset_request(request):
    """
    Запрос на восстановление пароля.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Форма запроса восстановления пароля
    """
    # Временная заглушка - будем развивать на следующем шаге
    return render(request, 'accounts/password_reset.html')


def password_reset_confirm(request, uidb64, token):
    """
    Подтверждение восстановления пароля.
    
    Args:
        request: HTTP запрос
        uidb64: Закодированный ID пользователя
        token: Токен восстановления
        
    Returns:
        HttpResponse: Форма установки нового пароля
    """
    # Временная заглушка - будем развивать на следующем шаге
    return render(request, 'accounts/password_reset_confirm.html')


def password_reset_done(request):
    """
    Страница уведомления об отправке письма восстановления пароля.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Страница уведомления
    """
    return render(request, 'accounts/password_reset_done.html')


def password_reset_complete(request):
    """
    Страница успешного восстановления пароля.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Страница успешного восстановления
    """
    return render(request, 'accounts/password_reset_complete.html')
