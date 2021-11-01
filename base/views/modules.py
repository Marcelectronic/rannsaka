from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views import View
from ..forms import ModuleForm
from ..models import Module
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.contrib import messages


# Class for the modules view
# Using the generic View
class ModulesView(LoginRequiredMixin, View):
    login_url = getattr(settings, "LOGIN_URL", None)

    # If method = GET return the default page
    def get(self, request):
        form = ModuleForm()
        return self.return_blank_page(request, form)

    # If method = POST
    def post(self, request):
        form = ModuleForm(request.POST)
        # If NEW
        if 'operation-new' in request.POST:
            return self.add_module(request, form)

    # Utility function to return the default page (module template)
    def return_blank_page(self, request, form):
        # Get all the modules
        modules = Module.objects.all().order_by('name')
        page_size = settings.PAGE_SIZE
        paginator = Paginator(modules, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'base/modules.html', {'modules': page_obj, 'form': form, 'page_obj': page_obj})

    # Add module
    def add_module(self, request, form):
        try:
            # Check of form is valid and save
            if form.is_valid():
                form.save()
            else:
                # If not valid returns default page with error msg
                messages.error(self.request, _('There was an error inserting to the database.'))
                return self.return_blank_page(request, form)
        except:
            # If unkown error returns default page with error msg
            messages.error(self.request, _('There was an error in the database.'))
            return self.return_blank_page(request, ModuleForm())
        else:
            # If no error returns default page with info
            messages.info(self.request, _('Info added to the database.'))
            return self.return_blank_page(request, ModuleForm())
