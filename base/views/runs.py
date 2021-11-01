from ..models import StreamRun
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.conf import settings


# View for the runs view
# Use the generic ListView
class RunsView(LoginRequiredMixin, ListView):
    LOGIN_URL = getattr(settings, "LOGIN_URL", None)
    login_url = LOGIN_URL
    paginate_by = settings.PAGE_SIZE

    # Use runs template
    template_name = 'base/runs.html'
    model = StreamRun
    # Set the name for the template's data
    context_object_name = 'runs'

    # Override the get data function (for sorting)
    def get_queryset(self, **kwargs):
        base_query = super().get_queryset()
        return base_query.order_by('-end')
