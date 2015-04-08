from django.conf import settings


def rollbar(request):
    if hasattr(settings, 'ROLLBAR'):
        return {
            'ROLLBAR_CONFIG': {
                'accessToken': "26890d87531840648300ef2e861002aa",
                'captureUncaught': True,
                'payload': {
                    'environment': settings.ROLLBAR['environment'],
                },
            },
        }
    return {}
