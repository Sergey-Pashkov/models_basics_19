"""
Настройки административной панели для приложения accounts.

Содержит конфигурацию для управления пользователями
через Django Admin.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Кастомная административная панель для модели CustomUser.
    
    Адаптирует стандартный UserAdmin для работы с нашей
    кастомной моделью пользователя.
    """
    
    # Поля, отображаемые в списке пользователей
    list_display = (
        'email',
        'first_name', 
        'last_name',
        'phone_number',
        'is_active',
        'email_confirmed',
        'is_staff',
        'date_joined'
    )
    
    # Поля для фильтрации в боковой панели
    list_filter = (
        'is_active',
        'email_confirmed',
        'is_staff',
        'is_superuser',
        'date_joined'
    )
    
    # Поля для поиска
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'phone_number'
    )
    
    # Поля, доступные только для чтения
    readonly_fields = (
        'date_joined',
        'last_login',
        'last_login_ip'
    )
    
    # Порядок сортировки (новые пользователи первыми)
    ordering = ('-date_joined',)
    
    # Поля для редактирования отдельного пользователя
    fieldsets = (
        # Основная информация
        (None, {
            'fields': ('email', 'password')
        }),
        
        # Персональная информация
        (_('Персональная информация'), {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'address',
                'date_of_birth'
            )
        }),
        
        # Права доступа
        (_('Права доступа'), {
            'fields': (
                'is_active',
                'email_confirmed',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
            'classes': ('collapse',)  # Сворачиваемая секция
        }),
        
        # Важные даты и метаданные
        (_('Важные даты'), {
            'fields': (
                'last_login',
                'date_joined',
                'last_login_ip'
            ),
            'classes': ('collapse',)  # Сворачиваемая секция
        }),
    )
    
    # Поля для формы добавления нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'phone_number',
                'password1',
                'password2',
                'is_active',
                'email_confirmed'
            ),
        }),
    )
    
    # Действия, доступные для группы пользователей
    actions = [
        'activate_users',
        'deactivate_users',
        'confirm_emails',
        'make_staff'
    ]
    
    def activate_users(self, request, queryset):
        """
        Активирует выбранных пользователей.
        
        Args:
            request: HTTP запрос
            queryset: Выбранные пользователи
        """
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} пользователь(ей) было активировано.'
        )
    activate_users.short_description = "Активировать выбранных пользователей"
    
    def deactivate_users(self, request, queryset):
        """
        Деактивирует выбранных пользователей.
        
        Args:
            request: HTTP запрос
            queryset: Выбранные пользователи
        """
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} пользователь(ей) было деактивировано.'
        )
    deactivate_users.short_description = "Деактивировать выбранных пользователей"
    
    def confirm_emails(self, request, queryset):
        """
        Подтверждает email адреса выбранных пользователей.
        
        Args:
            request: HTTP запрос
            queryset: Выбранные пользователи
        """
        updated = queryset.update(email_confirmed=True)
        self.message_user(
            request,
            f'Email адреса {updated} пользователь(ей) были подтверждены.'
        )
    confirm_emails.short_description = "Подтвердить email выбранных пользователей"
    
    def make_staff(self, request, queryset):
        """
        Делает выбранных пользователей сотрудниками.
        
        Args:
            request: HTTP запрос
            queryset: Выбранные пользователи
        """
        updated = queryset.update(is_staff=True)
        self.message_user(
            request,
            f'{updated} пользователь(ей) получили права сотрудника.'
        )
    make_staff.short_description = "Сделать сотрудниками"
