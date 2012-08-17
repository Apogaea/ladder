from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Sends an email through the framework to an address specified on the command line."
    args = "<email email...>"
    can_import_settings = True

    def handle(self, *args, **kwargs):
        pass
