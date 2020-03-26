from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [

    # Levels
    path('class/<slug:level>/', views.level_detail, name='level_detail'),
]
