"""
URL конфигурация для приложения accounts.

Определяет маршруты для:
- Регистрации пользователей
- Входа и выхода из системы
- Активации аккаунтов
- Управления профилем
- Восстановления пароля
"""

from django.urls import path
from . import views

# Пространство имен для приложения
app_name = 'accounts'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # Регистрация и активация
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('email-confirmation-sent/', views.email_confirmation_sent, name='email_confirmation_sent'),
    
    # Вход и выход
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Профиль пользователя
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    
    # Восстановление пароля
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset-complete/', views.password_reset_complete, name='password_reset_complete'),
]
