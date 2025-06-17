# ai_utils.py

import os
from openai import OpenAI
from openai import OpenAIError

# Клієнт безпосередньо зчитує ключ з .env або змінної середовища
client = OpenAI()

def generate_tarot_prediction(card_name, card_description, is_reversed):
    """
    Генерує передбачення на основі карти Таро, її опису та положення.
    """

    orientation = "перевернута" if is_reversed else "пряма"
    prompt = (
        f"Карта дня: {card_name} ({orientation}). "
        f"Опис карти: {card_description}.\n"
        f"На основі цього, сформулюй індивідуальне передбачення на сьогодні "
        f"у стилі езотеричного гіда. "
        f"Уникай повтору опису карти. Обсяг тексту — приблизно 100 слів. "
        f"Пиши у доброзичливому, натхненному стилі."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти містичний гід, який створює езотеричні передбачення."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        message = response.choices[0].message.content.strip()
        print("🔮 Запит:", prompt)
        print("📝 Відповідь:", message)
        return message

    except OpenAIError as e:
        print("❌ Помилка OpenAI:", str(e))
        return "Не вдалося згенерувати передбачення. Спробуйте пізніше."
