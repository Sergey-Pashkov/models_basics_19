# 🛒 Django интернет-магазин - система аутентификации

Учебный проект Django с полнофункциональной системой регистрации и аутентификации пользователей.

## 📋 Описание проекта

Это демонстрационный проект интернет-магазина, созданный для изучения основ Django и системы аутентификации. Проект включает в себя:

- 👤 Кастомную модель пользователя
- 📧 Регистрацию с подтверждением email
- 🔐 Систему входа и выхода
- 🏠 Личный кабинет пользователя
- 🔑 Восстановление пароля (в разработке)
- 👑 Административную панель

## 📚 Обучающие материалы

### 📧 Понимание системы email:
- **[EMAIL_SYSTEM_EXPLAINED.md](EMAIL_SYSTEM_EXPLAINED.md)** - объяснение "на пальцах" с простыми аналогиями
- **[REGISTRATION_FLOW_DIAGRAM.md](REGISTRATION_FLOW_DIAGRAM.md)** - визуальные схемы и диаграммы процесса
- **[demo_registration_explained.py](demo_registration_explained.py)** - интерактивная демонстрация работы системы

### 🎯 Рекомендуемый порядок изучения:
1. 📖 Прочитайте [EMAIL_SYSTEM_EXPLAINED.md](EMAIL_SYSTEM_EXPLAINED.md) - основы с аналогиями
2. 🔄 Изучите [REGISTRATION_FLOW_DIAGRAM.md](REGISTRATION_FLOW_DIAGRAM.md) - визуальные схемы
3. 🎭 Запустите `python demo_registration_explained.py` - живая демонстрация
4. 🧪 Протестируйте сами через веб-интерфейс

## 🚀 Быстрый старт

### Требования

- Python 3.8+
- Django 4.2+
- SQLite (включен в Python)

### Установка

1. **Клонирование репозитория:**
   ```bash
   git clone git@github.com:Sergey-Pashkov/models_basics_19.git
   cd models_basics_19/django_shop
   ```

2. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Создание базы данных:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Создание суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Запуск сервера:**
   ```bash
   python manage.py runserver
   ```

5. **Открытие в браузере:**
   - Главная страница: http://127.0.0.1:8000/
   - Админ-панель: http://127.0.0.1:8000/admin/

## 📁 Структура проекта

```
django_shop/
├── manage.py                    # Основной файл управления Django
├── requirements.txt             # Зависимости проекта
├── demo_test.py                # Демонстрационный скрипт
├── db.sqlite3                  # База данных SQLite
├── shop_project/               # Основной пакет проекта
│   ├── __init__.py
│   ├── settings.py             # Настройки проекта
│   ├── urls.py                 # Основные URL маршруты
│   ├── wsgi.py                 # WSGI конфигурация
│   └── asgi.py                 # ASGI конфигурация
├── accounts/                   # Приложение для работы с пользователями
│   ├── __init__.py
│   ├── models.py               # Кастомная модель пользователя
│   ├── views.py                # Представления (регистрация, вход и т.д.)
│   ├── forms.py                # Формы регистрации и входа
│   ├── urls.py                 # URL маршруты приложения
│   ├── admin.py                # Настройки админ-панели
│   ├── apps.py                 # Конфигурация приложения
│   ├── tests.py                # Тесты приложения
│   └── migrations/             # Миграции базы данных
├── templates/                  # HTML шаблоны
│   ├── base.html               # Базовый шаблон
│   └── accounts/               # Шаблоны для приложения accounts
│       ├── home.html           # Главная страница
│       ├── register.html       # Страница регистрации
│       ├── login.html          # Страница входа
│       ├── profile.html        # Личный кабинет
│       └── email/              # Шаблоны email писем
└── static/                     # Статические файлы (CSS, JS, изображения)
```

## 🔧 Функциональность

### ✅ Реализовано

#### 👤 Кастомная модель пользователя
- **Email как основное поле входа** (вместо username)
- **Дополнительные поля:** 
  - Номер телефона с валидацией
  - Адрес доставки
  - Дата рождения
  - Статус подтверждения email
  - IP адрес последнего входа
- **Методы модели:**
  - `get_full_name()` - полное имя
  - `get_short_name()` - короткое имя
  - `can_login()` - проверка возможности входа

#### 📝 Система регистрации
- **Форма регистрации** с валидацией
- **Отправка email с активацией** (HTML + текст)
- **Проверка уникальности email**
- **Валидация номера телефона** (российский формат)
- **Согласие с условиями использования**

#### 🔐 Система входа
- **Аутентификация по email**
- **Проверка статуса аккаунта** (активность, подтверждение email)
- **Функция "Запомнить меня"** (30 дней)
- **Запись IP адреса входа**
- **Подробные сообщения об ошибках**

#### 🏠 Личный кабинет
- **Информация о пользователе**
- **Статистика заказов** (заглушка)
- **Управление адресами доставки**
- **Ссылки на редактирование профиля**

#### 👑 Административная панель
- **Кастомный интерфейс** для управления пользователями
- **Фильтры и поиск** по различным полям
- **Массовые действия** (активация, подтверждение email)
- **Группировка полей** по категориям

#### 🎨 Интерфейс
- **Bootstrap 5** для современного дизайна
- **Адаптивная верстка** для мобильных устройств
- **JavaScript валидация** форм в реальном времени
- **Информативные сообщения** и подсказки

### 🚧 В разработке

- 🔑 Восстановление пароля
- ✏️ Редактирование профиля
- 🔄 Изменение пароля
- 🗑️ Удаление аккаунта
- 🛒 Интеграция с корзиной покупок

## 🧪 Тестирование

### Запуск unit-тестов
```bash
python manage.py test accounts
```

### Демонстрационный скрипт
```bash
python demo_test.py
```

Демонстрационный скрипт проверяет:
- ✅ Создание пользователей
- ✅ Генерацию токенов активации
- ✅ Методы модели пользователя
- ✅ Работу менеджера пользователей
- ✅ Статистику пользователей

## 📧 Настройка Email

### ⚠️ Важно: Email в режиме разработки

**В режиме разработки все email отправляются в консоль Django сервера!**

📋 **Как увидеть письма активации:**

1. **Запустите Django сервер:**
   ```bash
   python manage.py runserver
   ```

2. **В том же терминале** будут появляться все отправляемые письма:
   ```
   Content-Type: text/plain; charset="utf-8"
   Subject: Подтверждение регистрации в интернет-магазине
   From: noreply@shop.local
   To: user@example.com
   
   Добро пожаловать в Интернет-магазин!
   [... текст письма с ссылкой активации ...]
   ```

3. **Скопируйте ссылку активации** из письма и откройте в браузере

4. **Пример письма в консоли:**
   - Письмо содержит как текстовую, так и HTML версию
   - Ссылка активации имеет вид: `http://localhost:8000/activate/UID/TOKEN/`
   - Письмо отправляется сразу после регистрации

### 🧪 Тестирование email системы

```bash
# Простой тест отправки email
python test_email.py

# Создание пользователя и отправка письма активации
python test_user_email.py

# Мониторинг email системы
python email_monitor.py
```

### Для разработки (консольный вывод) - используется по умолчанию
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@shop.local'
```

### Для продакшена (например, Gmail)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Используйте пароль приложения!
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Альтернативные SMTP настройки

**Yandex Mail:**
```python
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@yandex.ru'
EMAIL_HOST_PASSWORD = 'your-password'
```

**Mail.ru:**
```python
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@mail.ru'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🔒 Безопасность

Проект включает следующие меры безопасности:

- ✅ **CSRF защита** для всех форм
- ✅ **Хеширование паролей** Django
- ✅ **Валидация паролей** (длина, сложность)
- ✅ **Проверка подтверждения email** перед входом
- ✅ **Токены активации** с ограниченным сроком действия
- ✅ **XSS защита** в шаблонах
- ✅ **Валидация данных** на уровне модели и форм

## 🎯 Использование

### Регистрация нового пользователя
1. Перейдите на `/register/`
2. Заполните форму регистрации
3. **Проверьте консоль Django сервера** - там появится письмо с активацией
4. **Скопируйте ссылку активации** из письма в консоли
5. Перейдите по ссылке активации в браузере
6. Войдите в систему

**💡 Важно:** Письма НЕ приходят на реальную почту - они отображаются в консоли!

### Вход в систему
1. Перейдите на `/login/`
2. Введите email и пароль
3. При желании отметьте "Запомнить меня"
4. Нажмите "Войти в систему"

### Административная панель
1. Перейдите на `/admin/`
2. Войдите как суперпользователь
3. Управляйте пользователями в разделе "Accounts"

## 📚 Технические детали

### Используемые технологии
- **Backend:** Django 4.2
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **База данных:** SQLite (разработка), PostgreSQL (продакшен)
- **Email:** Django email framework
- **Валидация:** Django forms + JavaScript

### Ключевые особенности кода
- **Подробные комментарии** на русском языке
- **Docstrings** для всех функций и классов
- **Type hints** где применимо
- **Обработка ошибок** с информативными сообщениями
- **Логирование** важных событий
- **Тесты** для основной функциональности

## 🤝 Развитие проекта

Следующие этапы развития:
1. **Восстановление пароля** - полная реализация
2. **Редактирование профиля** - формы и валидация
3. **Корзина покупок** - интеграция с пользователями
4. **Система заказов** - оформление и обработка
5. **Отзывы и рейтинги** - пользовательский контент
6. **API** - REST API для мобильных приложений

## 📞 Поддержка

Если у вас есть вопросы или предложения:
- Создайте issue в репозитории
- Отправьте pull request с улучшениями
- Свяжитесь с разработчиком

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

```
MIT License

Copyright (c) 2025 Sergey Pashkov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**📝 Примечание:** Это учебный проект, созданный для демонстрации возможностей Django. Не используйте его в продакшене без дополнительной настройки безопасности и оптимизации.

**🎓 Цель проекта:** Изучение Django, системы аутентификации, и лучших практик веб-разработки.
