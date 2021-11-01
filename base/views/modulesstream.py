from django.shortcuts import render
from django.views import View
from ..models import Stream, StreamModule, Module
from ..forms import StreamModuleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models import Max, F
from django.db import transaction
from django.utils.translation import gettext as _
from django.contrib import messages


# View for the modules of a stream
# Using the generic view
class ModulesStream(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    # If method = GET
    def get(self, request, slug):
        # Get stream using slug
        stream = Stream.objects.get(slug=slug)
        return self.return_with_blank(stream, request)

    # If method = POST
    def post(self, request, slug):
        # Get stream using slug
        stream = Stream.objects.get(slug=slug.lower())
        # If ADD
        if 'operation-new' in request.POST:
            return self.add_new(slug, stream, request)
        # if UPDATE
        else:
            return self.update_record(request, stream, slug)

    # Get the list of all modules
    def _get_options(self):
        options = []
        for module in Module.objects.all().order_by("name"):
            options.append((module.module_id, module.name,))
        return options

    # Add module to streams
    def add_new(self, slug, stream, request):
        # get all modules
        options = self._get_options()
        # Get the form
        form = StreamModuleForm(request.POST, choices=options)

        if form.is_valid():
            # Get form's module
            module = Module.objects.get(module_id=form.cleaned_data["module"])
            # Check if module already exist
            exist = StreamModule.objects.filter(stream_id=stream, module_id=module).count()
            if exist == 0:
                entered_order = form.cleaned_data["order"]
                try:
                    with transaction.atomic():
                        # Calculate current order
                        max_order = StreamModule.objects.filter(stream_id=
                                                                stream.stream_id).aggregate(Max("order"))["order__max"]
                        max_order = 0 if max_order is None else max_order
                        # If order is above max , set as max + 1
                        if entered_order >= max_order:
                            entered_order = max_order + 1
                        else:
                            # if order in between, update all modules's order above the entered data
                            StreamModule.objects.filter(stream_id=stream.stream_id, order__gte=entered_order). \
                                update(order=F('order') + 1)
                        # Create a stream module and save it to the db
                        StreamModule(stream_id=stream, module_id=module, order=entered_order).save()
                except:
                    # Unknown error , return default page with error msg
                    messages.error(self.request, _('There was an error in the database.'))
                    return self.return_with_blank(stream, request)
                else:
                    # No error, return default page with info msg
                    messages.info(self.request, _('Info added to the database.'))
                    return self.return_with_blank(stream, request)
            # Module already exist return default page with error msg
            else:
                messages.error(self.request, _('Module already exist!.'))
                return self.return_with_blank(stream, request)
        # Form is not valid return default page with error msg
        else:
            messages.error(self.request, _('Form is not valid.'))
            return self.return_with_blank(stream, request)

    # Update modules
    def update_record(self, request, stream, slug):
        try:
            # Get module id from form
            module_id = int(request.POST.get('module-id', '-1'))
        except ValueError:
            module_id = None

        try:
            # Get order from form
            order = int(request.POST.get('module-order', '-1'))
        except ValueError:
            order = None

        module = Module.objects.filter(module_id=module_id)[0]
        # Calcule max order value
        max_order = StreamModule.objects.filter(stream_id=
                                                stream.stream_id).aggregate(Max("order"))["order__max"]
        try:
            # Set transaction (all or nothing)
            with transaction.atomic():
                # Delete module
                if 'operation-delete' in request.POST:
                    StreamModule.objects.get(module_id=module, stream_id=stream, order=order).delete()
                    StreamModule.objects.filter(stream_id=stream, order__gte=order). \
                        update(order=F('order') - 1)

                # Move module up
                if 'operation-moveup' in request.POST:
                    if order >= 2:
                        module_down = StreamModule.objects.get(stream_id=stream, order=(order - 1)).module_id
                        StreamModule.objects.filter(module_id=module_down, stream_id=stream). \
                            update(order=F('order') + 1)
                        StreamModule.objects.filter(module_id=module, stream_id=stream).\
                            update(order=F('order') - 1)

                # Move module down
                if 'operation-movedown' in request.POST:
                    if order != max_order:
                        module_up = StreamModule.objects.get(stream_id=stream, order=(order + 1)).module_id
                        StreamModule.objects.filter(module_id=module_up, stream_id=stream). \
                            update(order=F('order') - 1)
                        StreamModule.objects.filter(module_id=module, stream_id=stream). \
                            update(order=F('order') + 1)
        # Unknown error, return default page with an error msg
        except:
            messages.error(self.request, _('There was an error in the database.'))
            return self.return_with_blank(stream, request)
        # No error, return default page with info msg
        else:
            if 'operation-delete' in request.POST:
                messages.info(self.request, _('Module deleted'))
            return self.return_with_blank(stream, request)

    # Return default page
    def return_with_blank(self, stream, request):
        # Filter modules
        modules = StreamModule.objects.filter(stream_id=stream.stream_id).order_by("order")
        options = self._get_options()
        # Set add form
        form = StreamModuleForm(choices=options, initial={'stream': stream.name, 'order': 1})
        return render(request, 'base/stream_modules.html', {'stream': stream, 'modules': modules,
                                                            'form': form})
