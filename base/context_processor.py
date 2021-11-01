from django.conf import settings


# Context processor for the breadcrumb path
# Store the path as list()
def breadcrumb_renderer(request):
    items = []
    components = filter(None, request.path.split('/'))
    path = ''
    for item in components:
        path = path + "/" + item
        items.append({'name': item, 'slug': path})
    return {
        'breadcrumbs': items
    }


# Context processor to return the dark mode status
# Retturn a Dict with status and name
def night_switch_renderer(request):
    if request.COOKIES.get(settings.NIGHT_SWITCH_NAME) == str(settings.NIGHT_SWITCH_ON):
        return {
            settings.NIGHT_SWITCH_NAME: settings.NIGHT_SWITCH_ON,
            settings.NIGHT_SWITCH_DOM: settings.NIGHT_SWITCH_NAME
        }
    else:
        return {
            settings.NIGHT_SWITCH_NAME: settings.NIGHT_SWITH_OFF,
            settings.NIGHT_SWITCH_DOM: settings.NIGHT_SWITCH_NAME
        }
