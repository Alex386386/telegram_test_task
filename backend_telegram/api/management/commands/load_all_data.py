import csv

from django.core.management import BaseCommand

from message.models import BotText


def iter_csv(file_path: str):
    with open(file_path, 'r', encoding="utf8") as inp_f:
        reader = csv.reader(inp_f)
        for row in reader:
            yield row


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = iter_csv('test_data/bot_messages.csv')
        for row in reader:
            text = BotText(title=row[0], text=row[1])
            text.save()
