from django.views.generic import DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings

User = get_user_model()

from betterforms.views import BrowseView

from ladder.core.decorators import AdminRequiredMixin

from ladder.apps.accounts.admin.forms import (
    UserChangeListForm,
    UserChangeForm,
)


class AdminUserListView(AdminRequiredMixin, BrowseView):
    template_name = 'accounts/admin/user_list.html'
    model = User
    form_class = UserChangeListForm
    paginate_by = settings.PAGINATE_BY


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
        return reverse('admin:user_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        profile = form.instance.profile
        profile.phone_number = form.cleaned_data['phone_number']
        profile.save()
        return super(AdminUserChangeView, self).form_valid(form)
