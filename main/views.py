import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .models import TarotCard, ReadingHistory, Rune, RuneReading
from .ai_utils import generate_tarot_prediction


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')


# ======= КАРТА ДНЯ =======

@login_required
def card_of_the_day(request):
    today = timezone.now().date()
    user = request.user

    # Перевіряємо, чи є вже карта для сьогодні
    prediction = ReadingHistory.objects.filter(user=user, drawn_at__date=today).first()

    already_drawn = prediction is not None

    if request.method == 'POST' and not already_drawn:
        card = random.choice(TarotCard.objects.all())
        is_reversed = random.choice([True, False])

        short_description = card.short_description_reversed if is_reversed else card.short_description
        full_description = card.full_description_reversed if is_reversed else card.full_description

        ai_prediction = generate_tarot_prediction(card.name, full_description, is_reversed)

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


# ======= ІСТОРІЯ КАРТ =======

@login_required
def reading_history(request):
    history = ReadingHistory.objects.filter(user=request.user).order_by('-drawn_at')
    return render(request, 'main/reading_history.html', {'history': history})


# ======= РУНА ДНЯ =======

@login_required
def rune_of_the_day(request):
    user = request.user
    today = timezone.localdate()

    reading = RuneReading.objects.filter(user=user, drawn_at__date=today).first()

    if reading:
        rune = reading.rune
        is_reversed = reading.is_reversed
        ai_prediction = reading.ai_prediction
        already_drawn = True
    else:
        rune = random.choice(Rune.objects.all())
        is_reversed = random.choice([True, False])
        full_text = rune.full_description_reversed if is_reversed else rune.full_description
        ai_prediction = f"Руна {rune.name} {'(перевернута)' if is_reversed else ''}: {full_text}"

        reading = RuneReading.objects.create(
            user=user,
            rune=rune,
            is_reversed=is_reversed,
            ai_prediction=ai_prediction
        )
        already_drawn = True

    return render(request, 'main/rune_of_the_day.html', {
        'rune': rune,
        'is_reversed': is_reversed,
        'short_description': rune.short_description_reversed if is_reversed else rune.short_description,
        'full_description': rune.full_description_reversed if is_reversed else rune.full_description,
        'ai_prediction': ai_prediction,
        'already_drawn': already_drawn
    })


# ======= ІСТОРІЯ РУН =======

@login_required
def rune_history(request):
    history = RuneReading.objects.filter(user=request.user).order_by('-drawn_at')
    return render(request, 'main/rune_history.html', {'history': history})
