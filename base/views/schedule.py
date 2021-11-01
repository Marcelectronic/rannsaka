from django.shortcuts import render
from django.views import View
from ..models import Schedule, SCHEDULE_STATUS_CHOICES
from ..forms import ScheduleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db import transaction


# View for the schedule page
# Using the generic View
class ScheduleView(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    # If method = GET return the default page
    def get(self, request):
        form = ScheduleForm()
        return self.return_blank_page(request, form)

    # If method = POST
    def post(self, request):
        form = ScheduleForm(request.POST)
        # If NEW
        if 'operation-new' in request.POST:
            return self.add_schedule(request, form)
        # If UPDATE
        elif 'operation-status' in request.POST:
            return self.update_schedule(request)

    # Utility function to return the default page (schedules template)
    def return_blank_page(self, request, form):
        # Get all the schedules
        schedules = Schedule.objects.all().order_by('schedule_id')
        # Get list with status options (css classes)
        parameters = self.get_choices()
        # add the choices (css classes) to the schedules
        for schedule in schedules:
            schedule.status_class, schedule.status_hide, schedule.status_btn, = \
                [(d['class'], d['hide'], d['btn-name'],) for d in parameters if d['name'] == schedule.status][0]
        return render(request, 'base/schedule.html', {'schedules': schedules, 'form': form})

    # Get the status options (css classes)
    def get_choices(self):
        parameters = []
        for choice in SCHEDULE_STATUS_CHOICES:
            if choice[0] == 'Disabled':
                parameters.append({'name': choice[0], 'class': 'text-danger', 'hide': '0', 'btn-name': _("Enable")})
            else:
                parameters.append({'name': choice[0], 'class': '', 'hide': '0', 'btn-name': _('Disable')})
        return parameters

    # Add stream
    def add_schedule(self, request, form):
        try:
            # Check of form is valid and save
            if form.is_valid():
                schedule = Schedule(
                    stream=form.cleaned_data['stream'],
                    start=form.cleaned_data['start'],
                    end=form.cleaned_data['end'],
                    period=form.cleaned_data['period'],
                    status=form.cleaned_data['status'],
                    run_type=form.cleaned_data['run_type']
                )
                schedule.save()
            else:
                # If not valid returns default page with error msg
                messages.error(self.request, _('Form is not valid.'))
                return self.return_blank_page(request, form)
        except:
            # If unkown error returns default page with error msg
            messages.error(self.request, _('There was an error in the database.'))
            return self.return_blank_page(request, ScheduleForm())
        else:
            # If no error returns default page with info
            messages.info(self.request, _('Info added to the database.'))
            return self.return_blank_page(request, ScheduleForm())

    # Update Schedule
    def update_schedule(self, request):
        try:
            # Set transaction (all or nothing)
            with transaction.atomic():
                if 'operation-status' in request.POST:
                    pk = request.POST.get('schedule-pk', '-1')
                    # Get schedule (using pk)
                    schedule = Schedule.objects.filter(pk=pk)[0]
                    # Change status and save
                    schedule.change_status()
                    schedule.save()
        except:
            # If there is an error return default page with an error msg
            messages.error(self.request, _('There was an error in the database.'))
            return self.return_blank_page(request, ScheduleForm())
        # If no error return default page with no error or info
        else:
            return self.return_blank_page(request, ScheduleForm())
