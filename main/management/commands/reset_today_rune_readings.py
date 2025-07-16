from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import RuneReading

class Command(BaseCommand):
    help = "Видаляє всі сьогоднішні записи RuneReading для перегенерації рун дня."

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        count = RuneReading.objects.filter(drawn_at__date=today).count()
        RuneReading.objects.filter(drawn_at__date=today).delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Видалено {count} сьогоднішніх RuneReading записів."))
