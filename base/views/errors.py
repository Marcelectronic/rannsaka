from ..models import ModuleError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.conf import settings


# Class for the errors view
# Use the generic ListView
class ErrorsView(LoginRequiredMixin, ListView):
    LOGIN_URL = getattr(settings, "LOGIN_URL", None)
    login_url = LOGIN_URL
    paginate_by = settings.PAGE_SIZE

    # Use runs template
    template_name = 'base/errors.html'
    model = ModuleError
    # Set the name for the template's data
    context_object_name = 'errors'

    # Override the get data function (for sorting)
    def get_queryset(self, **kwargs):
        base_query = super().get_queryset()
        return base_query.order_by('-moduleerror_id')
