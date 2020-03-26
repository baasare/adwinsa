from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'is_staff',)
    list_filter = ('email', 'username', 'is_staff', 'is_active',)

    fieldsets = ((None,
                  {'fields': (
                      'email', 'username', 'first_name', 'last_name', 'phone_number', 'password',)}),
                 ('Permissions', {'fields': ('is_staff', 'is_active', 'email_verified')}),
                 )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_staff',
                'is_active')}
         ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.site_header = "Adwinsa"
