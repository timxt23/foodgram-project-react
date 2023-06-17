import json
import os

from api.models import Ingredient
from django.conf import settings
from django.core.management.base import BaseCommand

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Импорт данных из файла json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        path = os.path.join(DATA_ROOT)
        with open(path, filename, 'r', encoding='utf-8') as f:
            ingredients = json.load(f)
            for ingredient in ingredients:
                name = ingredient.get('name')
                measurement_unit = ingredient.get('measurement_unit')
                if not Ingredient.objects.filter(name=name).exists():
                    Ingredient.objects.create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
