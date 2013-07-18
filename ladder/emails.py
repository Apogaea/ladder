from django.conf import settings
from emailtools import MarkdownEmail


class LadderEmail(MarkdownEmail):
    from_email = settings.DEFAULT_FROM_EMAIL
