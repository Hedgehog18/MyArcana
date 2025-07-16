from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import ReadingHistory

class Command(BaseCommand):
    help = "Видаляє всі сьогоднішні записи TarotReading (ReadingHistory), щоб перегенерувати карту дня."

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        count = ReadingHistory.objects.filter(drawn_at__date=today).count()
        ReadingHistory.objects.filter(drawn_at__date=today).delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Видалено {count} сьогоднішніх TarotReading записів."))
