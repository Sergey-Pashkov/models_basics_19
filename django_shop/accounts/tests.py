"""
Тесты для приложения accounts.

Содержит тесты для:
- Модели CustomUser
- Менеджера CustomUserManager
- Представлений (views)
- Форм регистрации и входа
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Получаем модель пользователя
User = get_user_model()


class CustomUserModelTest(TestCase):
    """Тесты для модели CustomUser."""
    
    def setUp(self):
        """Настройка данных для тестов."""
        self.email = 'test@example.com'
        self.password = 'testpassword123'
        
    def test_create_user(self):
        """Тест создания обычного пользователя."""
        user = User.objects.create_user(
            email=self.email,
            password=self.password
        )
        
        # Проверяем, что пользователь создан корректно
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)  # По умолчанию неактивен
        
    def test_create_superuser(self):
        """Тест создания суперпользователя."""
        user = User.objects.create_superuser(
            email=self.email,
            password=self.password
        )
        
        # Проверяем права суперпользователя
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        
    def test_create_user_without_email(self):
        """Тест создания пользователя без email."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password=self.password
            )
            
    def test_user_str_method(self):
        """Тест строкового представления пользователя."""
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name='Иван',
            last_name='Петров'
        )
        
        expected_str = f"Иван Петров ({self.email})"
        self.assertEqual(str(user), expected_str)
        
    def test_user_str_method_without_name(self):
        """Тест строкового представления пользователя без имени."""
        user = User.objects.create_user(
            email=self.email,
            password=self.password
        )
        
        self.assertEqual(str(user), self.email)
        
    def test_get_full_name(self):
        """Тест получения полного имени пользователя."""
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name='Иван',
            last_name='Петров'
        )
        
        self.assertEqual(user.get_full_name(), 'Иван Петров')
        
    def test_get_short_name(self):
        """Тест получения короткого имени пользователя."""
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name='Иван'
        )
        
        self.assertEqual(user.get_short_name(), 'Иван')
        
    def test_can_login_method(self):
        """Тест проверки возможности входа в систему."""
        user = User.objects.create_user(
            email=self.email,
            password=self.password
        )
        
        # Пользователь не может войти (неактивен и email не подтвержден)
        self.assertFalse(user.can_login())
        
        # Активируем пользователя и подтверждаем email
        user.is_active = True
        user.email_confirmed = True
        user.save()
        
        # Теперь пользователь может войти
        self.assertTrue(user.can_login())


class ViewsTest(TestCase):
    """Тесты для представлений (views)."""
    
    def setUp(self):
        """Настройка данных для тестов."""
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            is_active=True,
            email_confirmed=True
        )
        
    def test_home_view(self):
        """Тест главной страницы."""
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_register_view_get(self):
        """Тест GET запроса к странице регистрации."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        
    def test_login_view_get(self):
        """Тест GET запроса к странице входа."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        
    def test_profile_view_requires_login(self):
        """Тест требования авторизации для профиля."""
        response = self.client.get(reverse('accounts:profile'))
        # Должно перенаправить на страницу входа
        self.assertEqual(response.status_code, 302)
        
    def test_profile_view_for_authenticated_user(self):
        """Тест доступа к профилю для авторизованного пользователя."""
        # Входим в систему
        self.client.login(email='test@example.com', password='testpassword123')
        
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        
    def test_logout_view(self):
        """Тест выхода из системы."""
        # Входим в систему
        self.client.login(email='test@example.com', password='testpassword123')
        
        # Выходим
        response = self.client.get(reverse('accounts:logout'))
        
        # Должно перенаправить на главную страницу
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:home'))
