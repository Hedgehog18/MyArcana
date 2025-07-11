# main/models.py

from django.db import models
from django.contrib.auth.models import User


class TarotCard(models.Model):
    ARCANA_CHOICES = [
        ('Major', 'Старші аркани'),
        ('Minor', 'Молодші аркани'),
    ]

    SUIT_CHOICES = [
        ('Wands', 'Жезли'),
        ('Cups', 'Кубки'),
        ('Swords', 'Мечі'),
        ('Pentacles', 'Пентаклі'),
    ]

    name = models.CharField(max_length=100, verbose_name='Назва')
    arcana = models.CharField(max_length=10, choices=ARCANA_CHOICES, verbose_name='Аркана')
    suit = models.CharField(max_length=20, choices=SUIT_CHOICES, blank=True, null=True, verbose_name='Масть')
    number = models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер')
    short_description = models.TextField(verbose_name='Опис')
    full_description = models.TextField(blank=True, null=True, verbose_name='Повний опис')
    short_description_reversed = models.TextField(blank=True, null=True, verbose_name="Опис у перевернутому положенні")
    full_description_reversed = models.TextField(blank=True, null=True, verbose_name="Повний опис у перевернутому положенні")
    image = models.ImageField(upload_to='cards/', blank=True, null=True, verbose_name='Зображення')

    def __str__(self):
        return f"{self.name} ({self.arcana})"


class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    card = models.ForeignKey(TarotCard, on_delete=models.CASCADE)
    is_reversed = models.BooleanField(default=False)
    drawn_at = models.DateTimeField(auto_now_add=True)

    short_description = models.TextField()
    full_description = models.TextField()
    ai_prediction = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-drawn_at']

    def __str__(self):
        return f"{self.card.name} ({'перевернута' if self.is_reversed else 'пряма'}) - {self.drawn_at.date()}"


class Rune(models.Model):
    name = models.CharField(max_length=50, unique=True)
    short_description = models.TextField()
    full_description = models.TextField()
    short_description_reversed = models.TextField()
    full_description_reversed = models.TextField()
    image = models.ImageField(upload_to='runes/')

    def __str__(self):
        return self.name


class RuneOfTheDay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rune = models.ForeignKey(Rune, on_delete=models.CASCADE)
    drawn_at = models.DateTimeField(auto_now_add=True)
    is_reversed = models.BooleanField(default=False)

    def __str__(self):
        orientation = " (перевернута)" if self.is_reversed else ""
        return f"{self.user.username} - {self.rune.name}{orientation} - {self.drawn_at.date()}"
