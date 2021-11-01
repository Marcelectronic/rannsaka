from django.views.generic.edit import UpdateView
from ..models import Module
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from ..forms import ModuleForm
from django.utils.translation import gettext as _
from django.contrib import messages


# View for editing a module
# using the generic UpdateView
class EditModule(LoginRequiredMixin, UpdateView):
    login_url = getattr(settings, "LOGIN_URL", None)
    # Use module_edit template
    template_name = 'base/module_edit.html'
    model = Module
    # Use the ModuleForm
    form_class = ModuleForm
    # Return URL if success
    success_url = reverse_lazy('modules')

    # add error flags / msg to the template data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # if form is invalid
    def form_invalid(self, form):
        messages.error(self.request, _('Form is not valid.'))
        return super().form_invalid(form)

    # if form is valid
    def form_valid(self, form):
        messages.info(self.request, _('Info updated in the database.'))
        return super().form_valid(form)
