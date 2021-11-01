from django.contrib import admin
from .models import Stream
from .models import Module
from .models import StreamModule
from .models import StreamRun
from .models import ModuleRun
from .models import ModuleError
from .models import Schedule
from .models import Notification
# Register your models here.


class StreamAdmin(admin.ModelAdmin):
    list_filter = ("status", )
    list_display = ("stream_id", "name", "last_run", "next_run", "status", "slug","notification_to", "notification_cc",
                    "notification_type")


class ModuleAdmin(admin.ModelAdmin):
    list_display = ( "module_id", "name",  "file")


class StreamModuleAdmin(admin.ModelAdmin):
    list_display = ("stream_id", "module_id", "order")


class StreamRunAdmin(admin.ModelAdmin):
    list_display = ("run_id", "stream_id", "start", "end", "running", "errors")


class ModuleRunAdmin(admin.ModelAdmin):
    list_display = ("modulerun_id", "link_id", "run_id", "start", "end", "running", "errors")


class ModuleErrorAdmin(admin.ModelAdmin):
    list_display = ("moduleerror_id", "modulerun_id", "error_type", "error_row")


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("schedule_id", "stream", "start", "end", "period", "status", "run_type")


class NotificationAdmin(admin.ModelAdmin):
    list_filter = ("status",)
    list_display = ("notification_id", "to", "cc", "run_id", "sent", "status")


admin.site.register(Stream, StreamAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(StreamModule, StreamModuleAdmin)
admin.site.register(StreamRun, StreamRunAdmin)
admin.site.register(ModuleRun, ModuleRunAdmin)
admin.site.register(ModuleError, ModuleErrorAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Notification, NotificationAdmin)
