from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.conf import settings
from django.utils.translation import gettext as _
import csv
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from ..models import StreamRun, Stream, ModuleError, Notification


class ExportStreamRuns(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    def get(self, request, slug):
        stream = Stream.objects.get(slug=slug.lower())
        response = HttpResponse(
            content_type='text/csv', headers={'Content-Disposition': 'attachment; filename="runs_' +
                                                                     stream.name + '.csv"'}, )
        writer = csv.writer(response)
        stream_run = StreamRun.objects.filter(stream_id=stream).order_by('run_id')
        writer.writerow(['run_id', _('Start'), _('End'), _('Errors')])
        for run in stream_run:
            writer.writerow([run.run_id, run.start, run.end, run.errors])
        return response


class ExportRuns(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    def get(self, request):
        try:
            selected_date = request.GET.get("selected_date")
            if selected_date == '':
                return HttpResponseRedirect(reverse('runs'))
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except:
            return HttpResponseRedirect(reverse('runs'))
        response = HttpResponse(
            content_type='text/csv', headers={'Content-Disposition': 'attachment; filename="runs.csv"'}, )
        writer = csv.writer(response)
        stream_run = StreamRun.objects.filter(start__gte=selected_date).order_by('run_id')
        writer.writerow(['run_id',  _('Stream'), _('Start'), _('End'), _('Errors')])
        for run in stream_run:
            writer.writerow([run.run_id, run.stream_id.name, run.start, run.end, run.errors])
        return response


class ExportRunErrors(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    def get(self, request, slug):
        stream_run = StreamRun.objects.get(run_id=slug.lower())
        response = HttpResponse(
            content_type='text/csv', headers={'Content-Disposition': 'attachment; filename="run_errors_' +
                                                                     stream_run.stream_id.name + '.csv"'}, )
        writer = csv.writer(response)
        errors = ModuleError.objects.filter(modulerun_id__run_id=slug).order_by('-moduleerror_id')
        writer.writerow(['moduleerror_id', _('Module'), _('Type'), _('Row'), _('Data')])
        for error in errors:
            writer.writerow([error.moduleerror_id, error.modulerun_id.link_id.module_id.name, error.error_type,
                             error.error_row, error.error_data])
        return response


class ExportErrors(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    def get(self, request):
        try:
            selected_start = request.GET.get("selected_start")
            if selected_start == '':
                return HttpResponseRedirect(reverse('errors'))
            selected_start = int(selected_start)
        except:
            return HttpResponseRedirect(reverse('errors'))
        response = HttpResponse(
            content_type='text/csv', headers={'Content-Disposition': 'attachment; filename="errors.csv"'}, )
        writer = csv.writer(response)
        errors = ModuleError.objects.filter(moduleerror_id__gte=selected_start).order_by('moduleerror_id')
        writer.writerow(['moduleerror_id', _('Module'), _('Type'), _('Row'), _('Data')])
        for error in errors:
            writer.writerow([error.moduleerror_id, error.modulerun_id.link_id.module_id.name, error.error_type,
                             error.error_row, error.error_data])
        return response


class ExportNotifications(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    def get(self, request):
        try:
            selected_start = request.GET.get("selected_start")
            if selected_start == '':
                return HttpResponseRedirect(reverse('errors'))
            selected_start = int(selected_start)
        except:
            return HttpResponseRedirect(reverse('errors'))
        response = HttpResponse(
            content_type='text/csv', headers={'Content-Disposition': 'attachment; filename="notifications.csv"'}, )
        writer = csv.writer(response)
        notifications = Notification.objects.filter(notification_id__gte=selected_start).order_by('notification_id')
        writer.writerow(['notification_id', _('Stream'), _('To'), _('Cc'), _('Sent'), _('Status')])
        for notes in notifications:
            writer.writerow([notes.notification_id, notes.run_id.stream_id.name , notes.to, notes.cc, notes.sent,
                             notes.status])
        return response