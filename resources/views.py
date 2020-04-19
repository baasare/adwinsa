from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import Resource


@login_required
def level_detail(request, level):
    resources_list = Resource.objects.filter(level=level)

    page = request.GET.get('page', 1)

    paginator = Paginator(resources_list, 10)
    try:
        resources = paginator.page(page)
    except PageNotAnInteger:
        resources = paginator.page(1)
    except EmptyPage:
        resources = paginator.page(paginator.num_pages)

    if resources:
        current_level = resources[0].get_level_display
    else:
        current_level = "No Resource Available"
    return render(request, 'resources/level.html',
                  {'resources': resources, 'current_level': current_level, })
