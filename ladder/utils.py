from mock import patch
from contextlib import contextmanager

from django.utils import timezone


@contextmanager
def patch_now(when):
    with patch.object(timezone, 'now') as patched_now:
        patched_now.return_value = when
        yield
