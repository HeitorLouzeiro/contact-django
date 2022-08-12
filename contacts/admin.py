from django.contrib import admin

from .models import Contacts

# Register your models here.


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name',
                    'telephone', 'favorite', 'create')
    list_display_links = ('id', 'name',)
    list_editable = ('favorite',)
    list_filter = ('user', 'favorite',)
    list_per_page = 30


admin.site.register(Contacts, ContactsAdmin)
