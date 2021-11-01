from django import forms
from .models import Stream, Module, SCHEDULE_STATUS_CHOICES, SCHEDULE_TYPE_CHOICES, SCHEDULE_PERIOD_CHOICES
from django.utils.translation import ugettext_lazy as _


# ModelForm to insert / update the streams
class StreamForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['name', 'notification_type', 'notification_to', 'notification_cc']
        labels = {'name': _('Name'), 'notification_type': _('Notification Type'), 'notification_to': _('To'),
                  'notification_cc': _('Cc')}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'},),
                   'notification_type': forms.Select(attrs={'class': 'form-select'}, ),
                   'notification_to': forms.EmailInput(attrs={'class': 'form-control'}),
                   'notification_cc': forms.EmailInput(attrs={'class': 'form-control'})
                   }


class ScheduleForm(forms.Form):
    status = forms.ChoiceField(label=_('Status'), choices=SCHEDULE_STATUS_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    stream = forms.ModelChoiceField(label=_('Stream'), queryset=Stream.objects.all(), empty_label=None,
                                    widget=forms.Select(attrs={'class': 'form-select'}))
    run_type = forms.ChoiceField(label=_('Type'), choices=SCHEDULE_TYPE_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-select', 'onClick': 'typeHandler();',
                                                            'id': 'form_run_type'}))
    period = forms.ChoiceField(label=_('Period'), choices=SCHEDULE_PERIOD_CHOICES, required=False,
                               widget=forms.Select(attrs={'class': 'form-select', 'id': 'form_period'}))
    start = forms.DateTimeField(label=_('Start'), widget=forms.DateTimeInput(attrs={'type': 'datetime-local',
                                                                                    'class': 'form-control'}))
    end = forms.DateTimeField(label=_('End'), required=False, widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local', 'class': 'form-control', 'id': 'form_end'}))


# ModelForm to insert / update the modules
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'file', 'parameters']
        labels = {'name': _('Name'), 'template': _('Template'), 'parameters': _('Parameters'), 'file': _('File')}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}, ),
                   'template': forms.Select(attrs={'class': 'form-select'}, ),
                   'parameters': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}, ),
                   'file': forms.Select(attrs={'class': 'form-select'}, )}


# Form to add a module to a stream
class StreamModuleForm(forms.Form):

    stream = forms.CharField(label='Stream', disabled=True, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-select'}))
    module = forms.ChoiceField(label="Module",
                               widget=forms.TextInput(attrs={'class': 'form-select'}))
    order = forms.IntegerField(label='Order', required=True, max_value=100, min_value=1,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Set the module select (options and class)
    def __init__(self, *args, **kwargs):
        if 'choices' in kwargs:
            choices = kwargs.pop('choices')
        else:
            choices = []
        super(StreamModuleForm, self).__init__(*args, **kwargs)
        self.fields["module"] = forms.ChoiceField(label="Module", choices=choices)
        self.fields['module'].widget.attrs.update({'class': 'form-select'})
