from django.views.generic import (
    DetailView,
    UpdateView,
    FormView,
)
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings

from betterforms.views import BrowseView

from ladder.core.decorators import AdminRequiredMixin

from ladder.apps.accounts.admin.forms import (
    GeneratePreRegistrationUrlForm,
    UserChangeListForm,
    UserChangeForm,
)
from ladder.apps.accounts.utils import (
    reverse_pre_registration_url,
)

User = get_user_model()


class AdminUserListView(AdminRequiredMixin, BrowseView):
    template_name = 'accounts/admin/user_list.html'
    model = User
    form_class = UserChangeListForm
    paginate_by = settings.PAGINATE_BY


class AdminGeneratePreRegistrationLink(AdminRequiredMixin, FormView):
    form_class = GeneratePreRegistrationUrlForm
    template_name = 'accounts/admin/generate_pre_registration_link.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        token_url = self.request.build_absolute_uri(reverse_pre_registration_url(email))
        return self.render_to_response(self.get_context_data(form=form, token_url=token_url))


class AdminUserDetailView(AdminRequiredMixin, DetailView):
    template_name = 'accounts/admin/user_detail.html'
    model = User
    context_object_name = 'ladder_user'


class AdminUserChangeView(AdminRequiredMixin, UpdateView):
    template_name = 'accounts/admin/user_change.html'
    model = User
    form_class = UserChangeForm
    context_object_name = 'ladder_user'

    def get_success_url(self):
        return reverse('admin:user-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        profile = form.instance.profile
        profile.phone_number = form.cleaned_data['phone_number']
        profile.max_allowed_matches = form.cleaned_data['max_allowed_matches']
        profile.save()
        return super(AdminUserChangeView, self).form_valid(form)
