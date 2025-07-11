"""
Формы для приложения accounts.

Содержит формы для:
- Регистрации пользователей
- Входа в систему
- Редактирования профиля
- Изменения пароля
- Восстановления пароля
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

# Получаем модель пользователя
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма регистрации пользователя.
    
    Расширяет стандартную форму Django дополнительными полями
    и валидацией для нашей модели пользователя.
    """
    
    # Дополнительные поля формы
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        }),
        help_text='Введите действующий email адрес для активации аккаунта'
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        }),
        help_text='Имя (необязательно)'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваша фамилия'
        }),
        help_text='Фамилия (необязательно)'
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+79991234567'
        }),
        help_text='Номер телефона в формате +79991234567 (необязательно)'
    )
    
    address = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ваш адрес для доставки'
        }),
        help_text='Адрес доставки (необязательно)'
    )
    
    # Переопределяем поля паролей для добавления стилей
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        help_text='Пароль должен содержать минимум 8 символов'
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        }),
        help_text='Повторите пароль для подтверждения'
    )
    
    # Чекбокс согласия с условиями
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Я согласен с условиями использования и политикой конфиденциальности',
        error_messages={
            'required': 'Необходимо согласиться с условиями использования'
        }
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name', 
            'last_name',
            'phone_number',
            'address',
            'password1',
            'password2'
        )

    def __init__(self, *args, **kwargs):
        """Инициализация формы с дополнительными настройками."""
        super().__init__(*args, **kwargs)
        
        # Убираем стандартные help_text для паролей Django
        if 'password1' in self.fields:
            self.fields['password1'].help_text = 'Минимум 8 символов'
        if 'password2' in self.fields:
            self.fields['password2'].help_text = None

    def clean_email(self):
        """
        Валидация email адреса.
        
        Проверяет уникальность email в системе.
        
        Returns:
            str: Очищенный email адрес
            
        Raises:
            ValidationError: Если email уже существует
        """
        email = self.cleaned_data.get('email')
        
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(
                'Пользователь с таким email адресом уже существует. '
                'Попробуйте войти в систему или восстановить пароль.'
            )
        
        return email

    def clean_phone_number(self):
        """
        Валидация номера телефона.
        
        Returns:
            str: Очищенный номер телефона
            
        Raises:
            ValidationError: Если формат номера неверный
        """
        phone = self.cleaned_data.get('phone_number')
        
        if phone:
            # Убираем все символы кроме цифр и +
            cleaned_phone = ''.join(c for c in phone if c.isdigit() or c == '+')
            
            # Проверяем российский формат
            if not (cleaned_phone.startswith('+7') and len(cleaned_phone) == 12) and \
               not (cleaned_phone.startswith('7') and len(cleaned_phone) == 11) and \
               not (cleaned_phone.startswith('8') and len(cleaned_phone) == 11):
                raise ValidationError(
                    'Введите корректный российский номер телефона '
                    '(например: +79991234567, 79991234567 или 89991234567)'
                )
        
        return phone

    def save(self, commit=True):
        """
        Сохранение пользователя.
        
        Args:
            commit (bool): Сохранять ли объект в базе данных
            
        Returns:
            User: Объект пользователя
        """
        user = super().save(commit=False)
        
        # Устанавливаем дополнительные поля
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.address = self.cleaned_data.get('address', '')
        
        # Пользователь неактивен до подтверждения email
        user.is_active = False
        user.email_confirmed = False
        
        if commit:
            user.save()
        
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Кастомная форма входа в систему.
    
    Использует email вместо username и добавляет
    дополнительные проверки безопасности.
    """
    
    # Переопределяем поле username на email
    username = forms.EmailField(
        label='Email адрес',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com',
            'autofocus': True
        }),
        help_text='Введите ваш email адрес'
    )
    
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        help_text='Введите ваш пароль'
    )
    
    # Чекбокс "Запомнить меня"
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Запомнить меня'
    )

    def __init__(self, *args, **kwargs):
        """Инициализация формы."""
        super().__init__(*args, **kwargs)
        
        # Меняем лейбл поля username на email
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        self.fields['username'].label = 'Email адрес'

    def clean(self):
        """
        Валидация формы входа.
        
        Проверяет правильность email и пароля,
        а также статус аккаунта пользователя.
        
        Returns:
            dict: Очищенные данные формы
            
        Raises:
            ValidationError: При ошибках валидации
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            # Проверяем существование пользователя
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                raise ValidationError(
                    'Пользователь с таким email адресом не найден. '
                    'Проверьте правильность ввода или зарегистрируйтесь.'
                )
            
            # Проверяем, подтвержден ли email
            if not user.email_confirmed:
                raise ValidationError(
                    'Ваш email адрес не подтвержден. '
                    'Проверьте почту и перейдите по ссылке активации.'
                )
            
            # Проверяем, активен ли аккаунт
            if not user.is_active:
                raise ValidationError(
                    'Ваш аккаунт заблокирован. '
                    'Обратитесь к администратору сайта.'
                )
            
            # Аутентификация пользователя
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            
            if self.user_cache is None:
                raise ValidationError(
                    'Неверный email или пароль. '
                    'Попробуйте еще раз или восстановите пароль.'
                )

        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя.
    
    Позволяет пользователю изменять свою личную информацию,
    кроме email адреса и пароля.
    """
    
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text='Дата рождения для персональных предложений'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name', 
            'phone_number',
            'address',
            'date_of_birth'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша фамилия'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+79991234567'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ваш адрес для доставки'
            }),
        }

    def clean_date_of_birth(self):
        """
        Валидация даты рождения.
        
        Returns:
            date: Дата рождения
            
        Raises:
            ValidationError: Если дата некорректна
        """
        birth_date = self.cleaned_data.get('date_of_birth')
        
        if birth_date:
            # Проверяем, что дата не в будущем
            if birth_date > date.today():
                raise ValidationError('Дата рождения не может быть в будущем')
            
            # Проверяем минимальный возраст (13 лет)
            min_age_date = date.today().replace(year=date.today().year - 13)
            if birth_date > min_age_date:
                raise ValidationError('Минимальный возраст для регистрации: 13 лет')
            
            # Проверяем максимальный возраст (120 лет)
            max_age_date = date.today().replace(year=date.today().year - 120)
            if birth_date < max_age_date:
                raise ValidationError('Проверьте правильность введенной даты')
        
        return birth_date


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Кастомная форма изменения пароля.
    
    Добавляет Bootstrap стили к стандартной форме Django.
    """
    
    old_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текущий пароль'
        }),
        help_text='Введите ваш текущий пароль'
    )
    
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        }),
        help_text='Минимум 8 символов'
    )
    
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        }),
        help_text='Повторите новый пароль для подтверждения'
    )


class PasswordResetRequestForm(forms.Form):
    """
    Форма запроса восстановления пароля.
    
    Принимает email адрес для отправки ссылки восстановления.
    """
    
    email = forms.EmailField(
        label='Email адрес',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        }),
        help_text='Введите email адрес вашего аккаунта'
    )

    def clean_email(self):
        """
        Валидация email для восстановления пароля.
        
        Returns:
            str: Email адрес
            
        Raises:
            ValidationError: Если пользователь не найден
        """
        email = self.cleaned_data.get('email')
        
        if email:
            try:
                user = User.objects.get(email=email, is_active=True)
                if not user.email_confirmed:
                    raise ValidationError(
                        'Ваш email адрес не подтвержден. '
                        'Сначала активируйте аккаунт.'
                    )
            except User.DoesNotExist:
                raise ValidationError(
                    'Пользователь с таким email адресом не найден '
                    'или аккаунт не активирован.'
                )
        
        return email


class AccountDeletionForm(forms.Form):
    """
    Форма подтверждения удаления аккаунта.
    
    Требует подтверждения пароля для безопасности.
    """
    
    password = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль'
        }),
        help_text='Введите ваш пароль для подтверждения удаления аккаунта'
    )
    
    confirmation = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Я понимаю, что удаление аккаунта необратимо',
        error_messages={
            'required': 'Необходимо подтвердить понимание последствий'
        }
    )

    def __init__(self, user, *args, **kwargs):
        """
        Инициализация формы.
        
        Args:
            user: Текущий пользователь
        """
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        """
        Валидация пароля.
        
        Returns:
            str: Пароль
            
        Raises:
            ValidationError: Если пароль неверный
        """
        password = self.cleaned_data.get('password')
        
        if password and not self.user.check_password(password):
            raise ValidationError('Неверный пароль')
        
        return password
