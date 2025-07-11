# 📚 Models Basics 19 - Django Learning Repository

Учебный репозиторий для изучения основ Django и работы с моделями.

## 📁 Содержимое репозитория

### 🛒 [Django Shop](django_shop/)
Полнофункциональный Django проект интернет-магазина с системой аутентификации:

- 👤 Кастомная модель пользователя
- 📧 Регистрация с подтверждением email  
- 🔐 Система входа и выхода
- 🏠 Личный кабинет пользователя
- 👑 Административная панель
- 🧪 Полное покрытие тестами
- 📖 Подробная документация

#### 📚 Дополнительная документация:
- 📧 [EMAIL_SYSTEM_EXPLAINED.md](django_shop/EMAIL_SYSTEM_EXPLAINED.md) - объяснение системы email "на пальцах"
- 🔄 [REGISTRATION_FLOW_DIAGRAM.md](django_shop/REGISTRATION_FLOW_DIAGRAM.md) - визуальные схемы процесса регистрации
- 🎭 [demo_registration_explained.py](django_shop/demo_registration_explained.py) - живая демонстрация работы системы

**[➡️ Перейти к Django Shop](django_shop/)**

### 📓 [Jupyter Notebook](DZ_Pro.ipynb)
Дополнительные материалы и примеры кода для изучения.

## 🚀 Быстрый старт

```bash
# Клонирование репозитория
git clone git@github.com:Sergey-Pashkov/models_basics_19.git
cd models_basics_19

# Переход к Django проекту
cd django_shop

# Установка зависимостей
pip install -r requirements.txt

# Запуск проекта
python manage.py migrate
python manage.py runserver
```

## 🎓 Цели обучения

- Изучение основ Django framework
- Работа с моделями и ORM
- Создание системы аутентификации
- Работа с формами и валидацией
- Тестирование Django приложений
- Лучшие практики веб-разработки

## 📄 Лицензия

Проект распространяется под лицензией MIT. См. [LICENSE](django_shop/LICENSE) для деталей.

---

**👨‍💻 Автор:** Sergey Pashkov  
**📅 Дата создания:** Июль 2025  
**🎯 Назначение:** Учебный проект
