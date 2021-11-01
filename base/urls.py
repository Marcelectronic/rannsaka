from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from .views import streams, modulesstream, views, runstream, editstream, runbymodule, runs, errorsbymodule, \
    errorsbyrun, errors, modules, editmodule, schedule, editschedule, notifications, export

urlpatterns = [
    # Streams
    path('streams/', streams.StreamsView.as_view(), name='streams'),
    path('streams/modules/', RedirectView.as_view(url=reverse_lazy('streams'), permanent=False),
         name='modules_redirect'),
    path('streams/modules/<slug:slug>/', modulesstream.ModulesStream.as_view(), name='modules_stream'),
    path('streams/edit/', RedirectView.as_view(url=reverse_lazy('streams'), permanent=False),
         name='editstream_redirect'),
    path('streams/edit/<slug:slug>/', editstream.EditStream.as_view(), name='edit_stream'),
    path('streams/runs/', RedirectView.as_view(url=reverse_lazy('streams'), permanent=False),
         name='runs_redirect'),
    path('streams/runs/<slug:slug>/', runstream.RunsStream.as_view(), name='runs_stream'),
    path('streams/export/<slug:slug>/', export.ExportStreamRuns.as_view(), name='streamruns_export'),

    # Runs
    path('runs/', runs.RunsView.as_view(), name='runs'),
    path('runs/export/', export.ExportRuns.as_view(), name='runs_export'),
    path('runs/stream/<slug:slug>/', runbymodule.RunByModuleView.as_view(), name='run_module'),
    path('runs/moduleerrors/<slug:slug>/', errorsbymodule.ErrorsByModuleView.as_view(), name='modulerun_error'),
    path('runs/errors/<slug:slug>/', errorsbyrun.ErrorsByRunView.as_view(), name='run_error'),
    path('runs/errors/export/<slug:slug>/', export.ExportRunErrors.as_view(), name='export_run_error'),

    # Errors
    path('errors/', errors.ErrorsView.as_view(), name='errors'),
    path('errors/export/', export.ExportErrors.as_view(), name='errors_export'),

    # Modules
    path('modules/', modules.ModulesView.as_view(), name='modules'),
    path('modules/edit/<int:pk>/', editmodule.EditModule.as_view(), name='edit_module'),

    # Schedule
    path('schedule/', schedule.ScheduleView.as_view(), name='schedule'),
    path('schedule/edit/<int:pk>/', editschedule.EditSchedule.as_view(), name='edit_schedule'),

    # Notifications
    path('notifications/', notifications.NotificationsView.as_view(), name='notifications'),
    path('notifications/export/', export.ExportNotifications.as_view(), name='notifications_export'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Change Language and Dark Mode
    path('setlang/', views.set_language, name='set_language'),
    path('setnight/', views.set_night, name='set_night'),

    # Default
    path('', views.index, name='index'),
]
# Set the cookie with the language
