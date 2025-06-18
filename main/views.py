# main/views.py

import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .models import TarotCard, ReadingHistory
from .ai_utils import generate_tarot_prediction


@login_required
def card_of_the_day(request):
    today = timezone.now().date()
    user = request.user

    try:
        prediction = ReadingHistory.objects.get(user=user, drawn_at__date=today)
        already_drawn = True
    except ReadingHistory.DoesNotExist:
        prediction = None
        already_drawn = False

    if request.method == 'POST' and not already_drawn:
        card = random.choice(TarotCard.objects.all())
        is_reversed = random.choice([True, False])
        short_description = card.short_description_reversed if is_reversed else card.short_description
        full_description = card.full_description_reversed if is_reversed else card.full_description

        ai_prediction = generate_tarot_prediction(card.name, full_description, is_reversed)

        # Створюємо запис в історії
        prediction = ReadingHistory.objects.create(
            user=user,
            card=card,
            is_reversed=is_reversed,
            short_description=short_description,
            full_description=full_description,
            ai_prediction=ai_prediction
        )
        already_drawn = True

    context = {
        'already_drawn': already_drawn,
        'card': prediction.card if prediction else None,
        'is_reversed': prediction.is_reversed if prediction else False,
        'short_description': prediction.short_description if prediction else '',
        'full_description': prediction.full_description if prediction else '',
        'ai_prediction': prediction.ai_prediction if prediction else '',
    }

    return render(request, 'main/card_of_the_day.html', context)


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')


@login_required
def reading_history(request):
    history = ReadingHistory.objects.filter(user=request.user).order_by('-drawn_at')
    return render(request, 'main/reading_history.html', {'history': history})
