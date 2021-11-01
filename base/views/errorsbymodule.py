from ..models import ModuleError, ModuleRun
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.conf import settings


# View for the errors by module view
# Use the generic ListView
class ErrorsByModuleView(LoginRequiredMixin, ListView):
    LOGIN_URL = getattr(settings, "LOGIN_URL", None)
    login_url = LOGIN_URL
    paginate_by = settings.PAGE_SIZE
    # Use runs template
    template_name = 'base/errors_by_module.html'
    model = ModuleError
    # Set the name for the template's data
    context_object_name = 'errors'

    # Override the get data function (for sorting)
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        base_query = super().get_queryset()
        return base_query.filter(modulerun_id=slug).order_by('-moduleerror_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'slug' in self.kwargs:
            slug = self.kwargs["slug"]
        else:
            slug = None
        # use the slug to get the stream and add it
        run = ModuleRun.objects.get(modulerun_id=slug)
        context["run"] = run
        return context
