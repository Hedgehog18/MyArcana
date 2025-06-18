from django.core.management.base import BaseCommand
from main.models import TarotCard
from django.core.files.images import ImageFile
import json
from pathlib import Path

class Command(BaseCommand):
    help = 'Load tarot cards from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('--json', default='main/data/tarot_cards_uk.json')
        parser.add_argument('--images-dir', default='main/data/cards')

    def handle(self, *args, **options):
        json_path = Path(options['json'])
        images_dir = Path(options['images_dir'])
        with json_path.open(encoding='utf-8') as f:
            cards = json.load(f)

        name_map_major = {
            0: 'TheFool',
            1: 'TheMagician',
            2: 'TheHighPriestess',
            3: 'TheEmpress',
            4: 'TheEmperor',
            5: 'TheHierophant',
            6: 'TheLovers',
            7: 'TheChariot',
            8: 'Strength',
            9: 'TheHermit',
            10: 'WheelOfFortune',
            11: 'Justice',
            12: 'TheHangedMan',
            13: 'Death',
            14: 'Temperance',
            15: 'TheDevil',
            16: 'TheTower',
            17: 'TheStar',
            18: 'TheMoon',
            19: 'TheSun',
            20: 'Judgement',
            21: 'TheWorld',
        }

        for card in cards:
            tarot, created = TarotCard.objects.get_or_create(
                name=card['name'],
                defaults={
                    'arcana': card['arcana'],
                    'suit': card['suit'],
                    'number': card['number'],
                    'short_description': card['short_description'],
                    'full_description': None,
                    'short_description_reversed': card['short_description_reversed'],
                    'full_description_reversed': None,
                }
            )
            if created:
                image_file = None
                if card['arcana'] == 'Major':
                    idx = card['number']
                    fname = f"{idx:02d}-{name_map_major.get(idx)}.jpg"
                    image_file = images_dir / fname
                else:
                    fname = f"{card['suit']}{int(card['number']):02d}.jpg"
                    image_file = images_dir / fname
                if image_file and image_file.exists():
                    with open(image_file, 'rb') as imgf:
                        tarot.image.save(image_file.name, ImageFile(imgf), save=True)
        self.stdout.write(self.style.SUCCESS('Cards loaded'))

