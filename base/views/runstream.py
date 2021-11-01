from django.views.generic.list import ListView
from ..models import Stream, StreamRun
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


# View to show the runs of a stream
# using the generic ListView view
class RunsStream(LoginRequiredMixin, ListView):
    login_url = getattr(settings, "LOGIN_URL", None)
    model = StreamRun
    paginate_by = settings.PAGE_SIZE
    template_name = 'base/stream_runs.html'
    # set the template data's name
    context_object_name = 'runs'

    # modify the query to bring only the runs one stream
    def get_queryset(self):
        base_query = super().get_queryset()
        if 'slug' in self.kwargs:
            slug = self.kwargs["slug"]
        else:
            slug = None
        # Use the slug to get the stream
        stream = Stream.objects.get(slug=slug.lower())
        # Use the stream to get the runs
        return base_query.filter(stream_id=stream).order_by("-start")

    # add the stream to the templateś data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'slug' in self.kwargs:
            slug = self.kwargs["slug"]
        else:
            slug = None
        # use the slug to get the stream and add it
        stream = Stream.objects.get(slug=slug.lower())
        context["stream"] = stream
        return context
