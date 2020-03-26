from django.contrib import admin

from .models import Resource


@admin.register(Resource)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'level', 'strand', 'sub_strand', 'url',)
    list_filter = ('user', 'title', 'level', 'strand', 'sub_strand',)
    search_fields = ('title', 'level', 'strand')
    ordering = ('level', 'strand', 'sub_strand',)
    raw_id_fields = ('user',)


admin.site.site_header = "Adwinsa"
