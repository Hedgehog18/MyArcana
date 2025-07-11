import json
from django.core.management.base import BaseCommand
from main.models import Rune
from django.core.files.images import ImageFile
from pathlib import Path

class Command(BaseCommand):
    help = "Завантажує руни з JSON-файлу"

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Шлях до JSON файлу з рунами')

    def handle(self, *args, **options):
        json_file = options['json_file']
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            name = item['name']
            rune, created = Rune.objects.get_or_create(name=name)
            rune.short_description = item['short_description']
            rune.full_description = item['full_description']
            rune.short_description_reversed = item['short_description_reversed']
            rune.full_description_reversed = item['full_description_reversed']

            # додамо файл зображення
            image_path = Path("media") / item['image']
            if image_path.exists():
                with open(image_path, 'rb') as img_f:
                    rune.image.save(image_path.name, ImageFile(img_f), save=False)

            rune.save()

        self.stdout.write(self.style.SUCCESS("✅ Руни успішно імпортовані!"))
