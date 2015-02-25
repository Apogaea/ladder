from django.contrib.auth import logout as auth_logout


class LogoutIfInactiveMiddleware(object):
    def process_request(self, request):
        if not request.user.is_active:
            auth_logout(request)
