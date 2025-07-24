from django.contrib import admin
from .models import Book 
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from .models import CustomUser

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year' )
    list_filter = ('title', 'author') 
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin) 


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Add custom fields to the default fieldsets for editing existing users
    fieldsets = UserAdmin.fieldsets + (
        (gettext_lazy('Additional Info'), {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

    # Add custom fields when creating a new user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (gettext_lazy('Additional Info'), {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

    # Fields to display in list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
