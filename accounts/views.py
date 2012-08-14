from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

from accounts.forms import NewUserForm


class NewUserView(FormView):
    template_name = 'registration/new_user.html'
    form_class = NewUserForm
    success_url = lambda: reverse('new_user_success')

new_user = NewUserView.as_view()
