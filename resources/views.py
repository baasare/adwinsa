from django.shortcuts import render

from .models import Resource


# @login_required
def level_detail(request, level):
    resources = Resource.objects.filter(level=level)
    if resources:
        current_level = resources[0].get_level_display
    else:
        current_level = "No Resource Added"
    return render(request, 'resources/level.html', {'resources': resources, 'current_level': current_level})
