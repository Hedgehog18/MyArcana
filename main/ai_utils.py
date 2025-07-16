# ai_utils.py

from openai import OpenAI
from openai import OpenAIError
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam

client = OpenAI()

def generate_tarot_prediction(card_name: str, card_description: str, is_reversed: bool) -> str:
    """
    Генерує передбачення на основі карти Таро, її опису та положення.
    """

    orientation = "перевернута" if is_reversed else "пряма"
    prompt = (
        f"Карта дня: {card_name} ({orientation}). "
        f"Опис карти: {card_description}.\n"
        f"На основі цього сформулюй індивідуальне передбачення на сьогодні "
        f"у стилі езотеричного гіда. "
        f"Уникай прямого повтору назви чи опису карти. "
        f"Звертайся до користувача на 'Ви', використовуй форму 'Вам', 'Ваша', 'Вас'. "
        f"Не використовуй звернень типу 'мій шукачу', 'друже', 'ти'. "
        f"Текст має бути приблизно 100 слів, доброзичливим і натхненним, "
        f"без фамільярності, без панібратства. "
        f"Після складання передбачення, автоматично перевір його на стилістичні "
        f"та граматичні помилки українською мовою та виправ їх. "
        f"Надай вже виправлений текст."
    )

    messages: list[ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam] = [
        ChatCompletionSystemMessageParam(role="system", content="Ви містичний гід, який створює езотеричні передбачення."),
        ChatCompletionUserMessageParam(role="user", content=prompt)
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
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


def generate_rune_prediction(rune_name: str, rune_description: str, is_reversed: bool) -> str:
    """
    Генерує передбачення на основі руни, її опису та положення.
    """
    orientation = "перевернута" if is_reversed else "пряма"
    prompt = (
        f"Руна дня: {rune_name} ({orientation}). "
        f"Опис руни: {rune_description}.\n"
        f"На основі цього склади містичне індивідуальне передбачення для користувача на сьогодні. "
        f"Не повторюй дослівно назву чи опис руни. "
        f"Звертайся на 'Ви', використовуй слова 'Вам', 'Ваша', 'Вас'. "
        f"Не використовуй звернень на кшталт 'мій друже', 'шукачу', 'ти'. "
        f"Передбачення має бути близько 100 слів, спокійним, проникливим, "
        f"без фамільярності. "
        f"Після складання, уважно перевір та виправ стилістичні та граматичні помилки українською мовою."
        f"Надай вже виправлений текст."
    )

    messages: list[ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam] = [
        ChatCompletionSystemMessageParam(role="system", content="Ви містичний гід, який створює езотеричні передбачення."),
        ChatCompletionUserMessageParam(role="user", content=prompt)
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
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
