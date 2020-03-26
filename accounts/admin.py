from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import ugettext_lazy as _


class AccountsUserAdmin(UserAdmin):
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'contact_number', 'email')
    list_display = ('email', 'first_name', 'last_name', 'contact_number', 'is_staff', 'is_superuser')
    list_filter = ('groups', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'contact_number')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'minimum_download', 'groups')}),
        (_('Important dates'), {'fields': ('date_joined', 'deleted_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )


admin.site.register(User, AccountsUserAdmin)
