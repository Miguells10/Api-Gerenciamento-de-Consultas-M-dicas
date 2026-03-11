from django.contrib import admin

from .models import Professional


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ["social_name", "profession", "contact", "created_at"]
    search_fields = ["social_name", "profession"]
    readonly_fields = ["id", "created_at", "updated_at"]
