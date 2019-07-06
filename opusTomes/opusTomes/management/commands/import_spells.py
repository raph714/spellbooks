from django.core.management.base import BaseCommand
from django.utils import timezone
import json, os
from books.models import SRDPage

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(BASE_DIR, 'spells.json'), 'r') as f:
            datastore = json.load(f)

        #Use the new datastore datastructure
        for spell in datastore:
            casting_time = spell['casting_time']
            components = spell['components']['raw']
            description = spell['description']
            duration = spell['duration']
            name = spell['name']
            spell_range = spell['range']
            subtitle = spell['type']
            s = SRDPage(
                    title = name,
                    sub_title = subtitle,
                    casting_time = casting_time,
                    casting_range = spell_range,
                    components = components,
                    duration = duration,
                    description = description
                )
            s.save()
