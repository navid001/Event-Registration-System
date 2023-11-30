from django.contrib import admin
from .models import Event, Registration

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location_name', 'available_slots')
    search_fields = ('title', 'location_name')
    list_filter = ('date',)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registration_date')
    search_fields = ('user__username', 'event__title')
    list_filter = ('event__date', 'registration_date')

admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)



