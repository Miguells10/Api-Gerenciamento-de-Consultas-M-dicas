from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["professional", "date", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["professional__social_name"]
    readonly_fields = ["id", "created_at", "updated_at"]
