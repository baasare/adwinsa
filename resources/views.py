from django.shortcuts import render

from .models import Resource


# @login_required
def level_detail(request, level):
    resources = Resource.objects.filter(level=level)
    current_level = resources[0].get_level_display
    return render(request, 'resources/level.html', {'resources': resources, 'current_level': current_level})
