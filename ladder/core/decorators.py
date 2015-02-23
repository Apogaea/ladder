from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy

from authtools.views import DecoratorMixin


def user_is_admin(user):
    return user.is_admin


admin_required = user_passes_test(
    user_is_admin, login_url=reverse_lazy('admin:login'),
)


AdminRequiredMixin = DecoratorMixin(admin_required)
