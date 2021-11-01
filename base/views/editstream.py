from django.views.generic.edit import UpdateView
from ..models import Stream
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from ..forms import StreamForm
from django.contrib import messages
from django.utils.translation import gettext as _


# View for editing a stream
# using the generic UpdateView
class EditStream(LoginRequiredMixin, UpdateView):
    login_url = getattr(settings, "LOGIN_URL", None)
    # Use stream_edit template
    template_name = 'base/stream_edit.html'
    model = Stream
    # Use the StreamForm
    form_class = StreamForm
    # Return URL if success
    success_url = reverse_lazy('streams')

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
