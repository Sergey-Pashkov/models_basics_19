"""
Модели для приложения accounts.

Содержит кастомную модель пользователя с дополнительными полями
для интернет-магазина.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели пользователя.
    
    Обеспечивает создание пользователей и суперпользователей
    с email в качестве основного поля для входа.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя.
        
        Args:
            email (str): Email адрес пользователя
            password (str): Пароль пользователя
            **extra_fields: Дополнительные поля модели
            
        Returns:
            CustomUser: Созданный объект пользователя
            
        Raises:
            ValueError: Если email не указан
        """
        if not email:
            raise ValueError(_('Email адрес обязателен для заполнения'))
            
        # Нормализуем email (приводим домен к нижнему регистру)
        email = self.normalize_email(email)
        
        # Создаем объект пользователя
        user = self.model(email=email, **extra_fields)
        
        # Устанавливаем пароль (с хешированием)
        user.set_password(password)
        
        # Сохраняем пользователя в базе данных
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя.
        
        Args:
            email (str): Email адрес суперпользователя
            password (str): Пароль суперпользователя
            **extra_fields: Дополнительные поля модели
            
        Returns:
            CustomUser: Созданный объект суперпользователя
        """
        # Устанавливаем права суперпользователя
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Проверяем, что права установлены корректно
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя для интернет-магазина.
    
    Использует email вместо username для входа в систему.
    Содержит дополнительные поля для хранения информации
    о пользователе интернет-магазина.
    """
    
    # Валидатор для номера телефона (российский формат)
    phone_regex = RegexValidator(
        regex=r'^\+?7?[0-9]{10}$',
        message="Номер телефона должен быть в формате: '+79991234567' или '79991234567'"
    )
    
    # Основные поля пользователя
    email = models.EmailField(
        unique=True,
        verbose_name='Email адрес',
        help_text='Основной email для входа в систему'
    )
    
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Имя',
        help_text='Имя пользователя'
    )
    
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя'
    )
    
    # Дополнительные поля для интернет-магазина
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        verbose_name='Номер телефона',
        help_text='Номер телефона для связи и доставки'
    )
    
    address = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Адрес доставки',
        help_text='Полный адрес для доставки заказов'
    )
    
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
        help_text='Дата рождения для персональных предложений'
    )
    
    # Поля состояния аккаунта
    is_active = models.BooleanField(
        default=False,
        verbose_name='Аккаунт активен',
        help_text='Определяет, активен ли аккаунт (подтвержден ли email)'
    )
    
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус сотрудника',
        help_text='Определяет, может ли пользователь войти в админ-панель'
    )
    
    email_confirmed = models.BooleanField(
        default=False,
        verbose_name='Email подтвержден',
        help_text='Подтвержден ли email адрес пользователя'
    )
    
    # Временные метки
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации',
        help_text='Дата и время регистрации пользователя'
    )
    
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP последнего входа',
        help_text='IP адрес последнего входа в систему'
    )
    
    # Указываем кастомный менеджер
    objects = CustomUserManager()

    # Поле для аутентификации (вместо username используем email)
    USERNAME_FIELD = 'email'
    
    # Обязательные поля при создании суперпользователя
    REQUIRED_FIELDS = []

    class Meta:
        """Метаданные модели."""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']  # Сортировка по дате регистрации (новые первые)

    def __str__(self):
        """
        Строковое представление пользователя.
        
        Returns:
            str: Email пользователя или полное имя, если указано
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.email})"
        return self.email

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        
        Returns:
            str: Полное имя пользователя или email, если имя не указано
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.email

    def get_short_name(self):
        """
        Возвращает короткое имя пользователя.
        
        Returns:
            str: Имя пользователя или email, если имя не указано
        """
        return self.first_name or self.email

    def has_confirmed_email(self):
        """
        Проверяет, подтвержден ли email пользователя.
        
        Returns:
            bool: True, если email подтвержден, иначе False
        """
        return self.email_confirmed

    def can_login(self):
        """
        Проверяет, может ли пользователь войти в систему.
        
        Returns:
            bool: True, если пользователь может войти, иначе False
        """
        return self.is_active and self.email_confirmed
