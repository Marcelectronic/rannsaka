from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.utils import translation
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from ..models import ModuleRun, Notification, Schedule
from django.db.models import Count, Sum, Q
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from datetime import date, timedelta


# Home view, use the index template (dashboard)
def index(request):
    # graph colors
    background = [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)']
    border = [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ]

    # Calculate runs labels and data
    runs_labels = []
    runs_data = []

    runs_queryset = ModuleRun.objects.all().values(date_only=Cast('start', output_field=DateField())).\
        annotate(total=Count('modulerun_id')).order_by('-date_only')[:6]
    for item in runs_queryset:
        item_date = item['date_only'].strftime('%d-%m-%Y')
        runs_labels.append(item_date)
        runs_data.append(item['total'])

    # Fill in the data and graph values for runs
    runs_dataset = {"data": runs_data, "backgroundColor": background}
    runs_bordercolor = border

    # Calculate errors labels and data
    errors_labels = []
    errors_data = []

    errors_queryset = ModuleRun.objects.all().values(date_only=Cast('start', output_field=DateField())).\
        annotate(total=Sum('errors')).order_by('-date_only')[:6]
    for item in errors_queryset:
        item_date = item['date_only'].strftime('%d-%m-%Y')
        errors_labels.append(item_date)
        errors_data.append(item['total'])

    # Fill in the data and graph values for errors
    errors_dataset = {"data": errors_data, "backgroundColor": background}
    errors_bordercolor = border

    # Get the notifications las 7 days
    filter_week = date.today() - timedelta(days=7)
    notification_sent = Notification.objects.all().filter(Q(sent__gte=filter_week) & Q(status='Sent')).count()
    notification_notsent = Notification.objects.all().filter(Q(sent__gte=filter_week) & Q(status='Not Sent')).count()

    notifications = {
        "sent": notification_sent,
        "notsent": notification_notsent
    }

    # Get the next schedule stream
    filter_date = date.today()
    schedule_query = Schedule.objects.select_related().all().filter(Q(end__lt=filter_date)
                                                   & Q(status='Enabled')).order_by("-next_run")[0]
    schedule_next = schedule_query.stream.name

    # Get the schedule stream next 7 days
    filter_week = date.today() + timedelta(days=7)
    scheduled = Schedule.objects.select_related().all().filter(Q(end__lt=filter_date) &
                                                               Q(status='Enabled') &
                                                               Q(next_run__lte=filter_week)).count()

    schedule = {
        "next": schedule_next,
        "scheduled": scheduled
    }

    # Render page
    return render(request, 'base/index.html', {
        'runs_labels': runs_labels,
        'runs_data': runs_dataset,
        'runs_borderColor': runs_bordercolor,
        'errors_labels': errors_labels,
        'errors_data': errors_dataset,
        'errors_borderColor': errors_bordercolor,
        'notifications': notifications,
        'schedule': schedule
    })


# View to change profile attributes
@login_required
def profile(request):
    return render(request, 'base/profile.html')


# View to change the password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.info(request, _('Your password was successfully updated!'))
            return redirect(_('profile'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


# View to set the language
def set_language(request):
    if request.method == 'POST':
        # get the language from the form
        language = request.POST.get('language', settings.LANGUAGE_CODE)
        # Activate the new language
        translation.activate(language)
        # current URL to redirect to
        next_url = request.POST.get('next')
        if next_url:
            response = HttpResponseRedirect(next_url)
        else:
            response = redirect('index')
        # Set the cookie to the new language
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response


# View to set to Dark Mode
def set_night(request):
    if request.method == 'POST':
        # Get the new mode from the form
        night = request.POST.get(settings.NIGHT_SWITCH_NAME, settings.NIGHT_SWITH_OFF)
        # current URL to redirect to
        next_url = request.POST.get('next')
        if next_url:
            response = HttpResponseRedirect(next_url)
        else:
            response = redirect('index')
        # Set the cookie to the new dark mode
        response.set_cookie(settings.NIGHT_SWITCH_NAME, night)
        return response


# View for the login (dummy)
class MyLoginView(LoginView):
    pass

