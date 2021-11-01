from ..models import ModuleError, StreamRun
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.conf import settings


# View for the errors by run view
# Use the generic ListView
class ErrorsByRunView(LoginRequiredMixin, ListView):
    LOGIN_URL = getattr(settings, "LOGIN_URL", None)
    login_url = LOGIN_URL
    paginate_by = settings.PAGE_SIZE
    # Use runs template
    template_name = 'base/errors_by_run.html'
    model = ModuleError
    # Set the name for the template's data
    context_object_name = 'errors'

    # Override the get data function (for sorting)
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        base_query = super().get_queryset()
        return base_query.filter(modulerun_id__run_id=slug).order_by('-moduleerror_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'slug' in self.kwargs:
            slug = self.kwargs["slug"]
        else:
            slug = None
        # use the slug to get the stream and add it
        run = StreamRun.objects.get(run_id=slug)
        context["run"] = run
        return context
