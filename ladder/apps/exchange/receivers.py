from ladder.apps.exchange.model import LadderProfile


def create_ladder_profile(sender, instance, created, raw, **kwargs):
    if created and not raw:
        LadderProfile.objects.get_or_create(user=instance)
