from django.contrib import admin
from .models import TarotCard, ReadingHistory

@admin.register(TarotCard)
class TarotCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'arcana', 'suit', 'number')
    list_filter = ('arcana', 'suit')
    search_fields = ('name', 'description', 'full_description')
    fields = (
        'name',
        'arcana',
        'suit',
        'number',
        'description',
        'full_description',
        'reversed_description',
        'full_description_reversed',
        'image',
    )


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'drawn_at', 'is_reversed')
    list_filter = ('drawn_at', 'is_reversed')
    search_fields = ('user__username', 'card__name')
