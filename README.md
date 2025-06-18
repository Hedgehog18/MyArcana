# MyArcana

Цей проект — вебсайт на Django, що дозволяє виконувати розклади карт Таро і зберігати історію передбачень. Нижче наведено інструкцію з розгортання проекту на локальній машині під Windows 11.

## Вимоги

- **Python 3.11** або новіший (завантажити можна з [python.org](https://www.python.org/downloads/windows/))
- **Git** для отримання вихідного коду

## Кроки встановлення

1. **Клонування репозиторію**
   ```bash
   git clone <url_до_репозиторію>
   cd MyArcana
   ```

2. **Створення та активація віртуального середовища**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Встановлення залежностей**
   ```bash
   pip install -r requirements.txt
   ```

4. **Налаштування змінних середовища**
   Створіть файл `.env` у корені проекту і додайте у нього ваш ключ OpenAI:
   ```
   OPENAI_API_KEY=ваш_ключ
   ```
   Цей ключ використовується для генерації передбачень картами за допомогою API OpenAI.

5. **Міграції та створення суперкористувача**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Завантаження карт Таро** (одноразово)
   ```bash
   python manage.py load_tarot_cards
   ```
   Команда зчитає дані з `main/data/tarot_cards_uk.json` і пов'яже їх із зображеннями з `main/data/cards`.

7. **Запуск серверу розробки**
   ```bash
   python manage.py runserver
   ```
   Після запуску сайт буде доступний за адресою http://127.0.0.1:8000/

## Корисні посилання

- [Документація Django](https://docs.djangoproject.com/en/5.2/)
- [Створення віртуального середовища в Windows](https://docs.python.org/3/library/venv.html)

