import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import TarotCard


class Command(BaseCommand):
    help = "Завантажує карти Таро з JSON-файлу в базу даних"

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, "main", "data", "tarot_cards_uk.json")
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f"Файл не знайдено: {json_path}"))
            return

        with open(json_path, encoding="utf-8") as f:
            cards = json.load(f)

        created, updated = 0, 0

        for card in cards:
            obj, was_created = TarotCard.objects.update_or_create(
                name=card["name"],
                defaults={
                    "arcana": card["arcana"],
                    "suit": card.get("suit"),
                    "number": card.get("number"),
                    "short_description": card["short_description"],
                    "full_description": card["full_description"],
                    "short_description_reversed": card["short_description_reversed"],
                    "full_description_reversed": card["full_description_reversed"],
                    "image": card["image"],
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Імпорт завершено: створено {created}, оновлено {updated} карт."
        ))