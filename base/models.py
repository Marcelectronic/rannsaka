from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _
from django.conf import settings

# Choices for the status of streams
STATUS_CHOICES = [
    ('Running', 'Running'),
    ('Ready', 'Ready'),
    ('Disabled', 'Disabled'),
]

SCHEDULE_STATUS_CHOICES = [
    ('Enabled', 'Enabled'),
    ('Disabled', 'Disabled'),
]

SCHEDULE_TYPE_CHOICES = [
    ('Once', 'Once'),
    ('Unlimited', 'Unlimited'),
    ('Until', 'Until'),
]

SCHEDULE_PERIOD_CHOICES = [
    ('Every Month', 'Every Month'),
    ('Every Week', 'Every Week'),
    ('Every Weekday', 'Every Weekday'),
    ('Every Day', 'Every Day'),
    ('Every Day - Every 12 Hours', 'Every Day - Every 12 Hours'),
    ('Every Day - Every 8 Hours', 'Every Day - Every 8 Hours'),
    ('Every Day - Every 6 Hours', 'Every Day - Every 6 Hours'),
    ('Every Day - Every 4 Hours', 'Every Day - Every 4 Hours'),
    ('Every Day - Every 3 Hours', 'Every Day - Every 3 Hours'),
    ('Every Day - Every 2 Hours', 'Every Day - Every 2 Hours'),
    ('Every Day - Every 1 Hour', 'Every Day - Every 1 Hour'),
    ('Every Day - Every 30 Min.', 'Every Day - Every 30 Min.'),
    ('Every Day - Every 20 Min.', 'Every Day - Every 20 Min.'),
    ('Every Day - Every 15 Min.', 'Every Day - Every 15 Min.'),
    ('Every Day - Every 10 Min.', 'Every Day - Every 10 Min.'),
    ('Every Day - Every 5 Min', 'Every Day - Every 5 Min'),
    ('Every Weekday', 'Every Weekday'),
    ('Every Weekday - Every 12 Hours', 'Every Weekday - Every 12 Hours'),
    ('Every Weekday - Every 8 Hours', 'Every Weekday - Every 8 Hours'),
    ('Every Weekday - Every 6 Hours', 'Every Weekday - Every 6 Hours'),
    ('Every Weekday - Every 4 Hours', 'Every Weekday - Every 4 Hours'),
    ('Every Weekday - Every 3 Hours', 'Every Weekday - Every 3 Hours'),
    ('Every Weekday - Every 2 Hours', 'Every Weekday - Every 2 Hours'),
    ('Every Weekday - Every 1 Hour', 'Every Weekday - Every 1 Hour'),
    ('Every Weekday - Every 30 Min.', 'Every Weekday - Every 30 Min.'),
    ('Every Weekday - Every 20 Min.', 'Every Weekday - Every 20 Min.'),
    ('Every Weekday - Every 15 Min.', 'Every Weekday - Every 15 Min.'),
    ('Every Weekday - Every 10 Min.', 'Every Weekday - Every 10 Min.'),
    ('Every Weekday - Every 5 Min', 'Every Weekday - Every 5 Min'),
]

# Choices for stream running
RUNNING_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]

NOTIFICATION_CHOICES = [
    ('Sent', 'Sent'),
    ('Not Sent', 'Not Sent'),
]

NOTIFICATIONTYPE_CHOICES = [
    ('None', 'None'),
    ('Every Run', 'Every Run'),
    ('Every Run - When errors', 'Every Run - When errors'),
    ('Daily', 'Daily'),
    ('Daily - When errors', 'Daily - When errors'),
    ('Weekly Summary', 'Weekly Summary'),
]


# Function to validate if a stream status is within the allowed values
def validate_status(value):
    if value in ['Running', 'Ready', 'Disabled']:
        return value
    else:
        raise ValidationError(_("Wrong value"))


# Function to validate if a stream is running is within the allowed values
def validate_running(value):
    if value in ['Yes', 'No']:
        return value
    else:
        raise ValidationError(_("Wrong value"))


def script_path():
    return settings.SCRIPT_DIR


def jsonfield_default_value():
    return {"debug": 0}


# Model for the Streams.
class Stream(models.Model):
    stream_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    last_run = models.DateTimeField(null=True)
    next_run = models.DateTimeField(null=True)
    status = models.CharField(default='Ready', max_length=20, choices=STATUS_CHOICES)
    slug = models.SlugField(unique=True, blank=True,  db_index=True)
    notification_to = models.CharField(null=True, blank=True, max_length=200)
    notification_cc = models.CharField(null=True, blank=True, max_length=200)
    notification_type = models.CharField(default='None', max_length=50, choices=NOTIFICATIONTYPE_CHOICES)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def change_status(self):
        if self.status == 'Ready':
            self.status = 'Disabled'
        elif self.status == 'Disabled':
            self.status = 'Ready'


# Model for the Schedule.
class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name="Schedule_stream", null=False)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=True, blank=True)
    period = models.CharField(null=True, max_length=50, choices=SCHEDULE_PERIOD_CHOICES)
    status = models.CharField(null=False, max_length=20, choices=SCHEDULE_STATUS_CHOICES)
    run_type = models.CharField(null=False, max_length=20, choices=SCHEDULE_TYPE_CHOICES)
    next_run = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.stream}'

    def change_status(self):
        if self.status == 'Enabled':
            self.status = 'Disabled'
        elif self.status == 'Disabled':
            self.status = 'Enabled'


# Model for the modules
class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    streams = models.ManyToManyField(Stream, through='StreamModule', through_fields=('module_id', 'stream_id'))
    parameters = models.JSONField(null=False, default=jsonfield_default_value)
    file = models.FilePathField(path=script_path, unique=False, null=False)

    def __str__(self):
        return f'{self.name}'


# Model to link streams and modules (many to many)
class StreamModule(models.Model):
    stream_id = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name="StreamModule_stream_id")
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="StreamModule_module_id")
    order = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.module_id} ({self.stream_id}) - Order: {self.order}'


# Model for the stream's runs
class StreamRun(models.Model):
    run_id = models.AutoField(primary_key=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    running = models.CharField(default='YES', max_length=3, choices=RUNNING_CHOICES)
    errors = models.IntegerField(default=0)
    stream_id = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name="StreamRun_stream_id")

    def __str__(self):
        return f'{self.run_id} (Stream: {self.stream_id}) - {self.start}))'


# Model for the module's run
class ModuleRun(models.Model):
    modulerun_id = models.AutoField(primary_key=True)
    run_id = models.ForeignKey(StreamRun, on_delete=models.CASCADE,
                               related_name="ModuleRun_run_id")
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    running = models.BooleanField(default=True)
    errors = models.IntegerField(default=0)
    link_id = models.ForeignKey(StreamModule, on_delete=models.CASCADE, related_name="StreamRun")

    def __str__(self):
        return f'{self.modulerun_id} (Run:{self.run_id} - {self.start}))'


# Model for the module's errors
class ModuleError(models.Model):
    moduleerror_id = models.AutoField(primary_key=True)
    modulerun_id = models.ForeignKey(ModuleRun, on_delete=models.CASCADE,
                                     related_name="ModuleError_run_id")
    error_type = models.CharField(null=True, max_length=100)
    error_row = models.IntegerField(null=False, blank=True)
    error_data = models.TextField(null=False, blank=True, max_length=5000)

    def __str__(self):
        return f'{self.moduleerror_id} (Run:{self.modulerun_id} - {self.error_type}))'


# Model for the NOTIFICATIONS
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    to = models.CharField(null=False, max_length=200)
    cc = models.CharField(null=True, max_length=200)
    run_id = models.ForeignKey(StreamRun, on_delete=models.CASCADE, related_name="Notification_run_id")
    sent = models.DateTimeField(null=False)
    status = models.CharField(default='Sent', max_length=20, choices=NOTIFICATION_CHOICES)

    def __str__(self):
        return f'{self.notification_id}'
