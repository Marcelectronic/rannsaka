from django.shortcuts import render
from django.views import View
from ..models import Stream, STATUS_CHOICES
from ..forms import StreamForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db import transaction


# View for the streams page
# Using the generic View
class StreamsView(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    # If method = GET return the default page
    def get(self, request):
        form = StreamForm()
        return self.return_blank_page(request, form)

    # If method = POST
    def post(self, request):
        form = StreamForm(request.POST)
        # If NEW
        if 'operation-new' in request.POST:
            return self.add_stream(request, form)
        # If UPDATE
        elif 'operation-status' in request.POST:
            return self.update_stream(request)

    # Utility function to return the default page (streams template)
    def return_blank_page(self, request, form):
        # Get all the streams
        streams = Stream.objects.all().order_by('name')
        # Get list with status options (css classes)
        parameters = self.get_choices()
        # add the choices (css classes) to the streams
        for stream in streams:
            stream.status_class, stream.status_hide, stream.status_btn, = \
                [(d['class'], d['hide'], d['btn-name'],) for d in parameters if d['name'] == stream.status][0]
        return render(request, 'base/streams.html', {'streams': streams, 'form': form})

    # Get the status options (css classes)
    def get_choices(self):
        parameters = []
        for choice in STATUS_CHOICES:
            if choice[0] == 'Running':
                parameters.append({'name': choice[0], 'class': 'text-warning', 'hide': '1', 'btn-name': ''})
            elif choice[0] == 'Disabled':
                parameters.append({'name': choice[0], 'class': 'text-danger', 'hide': '0', 'btn-name': _("Enable")})
            else:
                parameters.append({'name': choice[0], 'class': '', 'hide': '0', 'btn-name': _('Disable')})
        return parameters

    # Add stream
    def add_stream(self, request, form):
        try:
            # Check of form is valid and save
            if form.is_valid():
                form.save()
            else:
                # If not valid returns default page with error msg
                messages.error(self.request, _('Form is not valid.'))
                return self.return_blank_page(request, form)
        except:
            # If unkown error returns default page with error msg
            messages.error(self.request, _('There was an error in the database.'))
            return self.return_blank_page(request, StreamForm())
        else:
            # If no error returns default page with info
            messages.info(self.request, _('Info added to the database.'))
            return self.return_blank_page(request, StreamForm())

    # Update Stream
    def update_stream(self, request):
        try:
            # Set transaction (all or nothing)
            with transaction.atomic():
                if 'operation-status' in request.POST:
                    slug = request.POST.get('stream-slug', '-1')
                    # Get stream (using slug)
                    stream = Stream.objects.filter(slug=slug)[0]
                    # Change status and save
                    stream.change_status()
                    stream.save()
        except:
            # If there is an error return default page with an error msg
            messages.error(self.request, _('There was an error in the database.'))
            return self.return_blank_page(request, StreamForm())
        # If no error return default page with no error or info
        else:
            return self.return_blank_page(request,  StreamForm())
