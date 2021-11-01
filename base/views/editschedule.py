from django.views.generic.edit import FormView
from ..models import Schedule
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from ..forms import ScheduleForm
from django.contrib import messages
from django.utils.translation import gettext as _


# View for editing a schedules
# using the generic FormView
class EditSchedule(LoginRequiredMixin, FormView):
    login_url = getattr(settings, "LOGIN_URL", None)
    # Use schedule_edit template
    template_name = 'base/schedule_edit.html'
    # Use the ScheduleForm
    form_class = ScheduleForm
    # Return URL if success
    success_url = reverse_lazy('schedule')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            pk = self.kwargs["pk"]
        else:
            pk = None
        schedule = Schedule.objects.get(schedule_id=pk)
        start = schedule.start.strftime('%Y-%m-%dT%H:%M')
        end = ''
        if schedule.end:
            end = schedule.end.strftime('%Y-%m-%dT%H:%M')
        form = ScheduleForm(initial={'status': schedule.status, 'stream': schedule.stream,
                                     'run_type': schedule.run_type, 'period': schedule.period,
                                     'start': start,
                                     'end': end})
        context['form'] = form
        return context

    # if form is invalid
    def form_invalid(self, form):
        messages.error(self.request, _('Form is not valid.'))
        return super().form_invalid(form)

    # if form is valid
    def form_valid(self, form):
        try:
            # Check of form is valid and save
            if form.is_valid():
                pk = None
                if 'pk' in self.kwargs:
                    pk = self.kwargs["pk"]
                schedule = Schedule.objects.get(pk=pk)
                schedule.stream = form.cleaned_data['stream']
                schedule.start = form.cleaned_data['start']
                schedule.end = form.cleaned_data['end']
                schedule.period = form.cleaned_data['period']
                schedule.status = form.cleaned_data['status']
                schedule.run_type = form.cleaned_data['run_type']
                schedule.save()
            else:
                # If not valid returns default page with error msg
                messages.error(self.request, _('Form is not valid.'))
                return super().form_invalid()
        except:
            # If unkown error returns default page with error msg
            messages.error(self.request, _('There was an error in the database.'))
            return super().form_invalid(form)
        else:
            # If no error returns default page with info
            messages.info(self.request, _('Info added to the database.'))
            return super().form_valid(form)


