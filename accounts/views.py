from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from accounts.forms import NewUserForm


class NewUserView(FormView):
    template_name = 'registration/new_user.html'
    form_class = NewUserForm
    success_url = lambda: reverse('new_user_success')
    success_url = '/account/new-user/'

    def get_form_kwargs(self):
        kwargs = super(NewUserView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user

        return kwargs

    def form_valid(self, form):
        form.save()
        return super(NewUserView, self).form_valid(form)

new_user = login_required(NewUserView.as_view())
