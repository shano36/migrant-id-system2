from django.contrib import admin
from .models import MigrantWorker
from django.contrib import admin
from .models import Application
from django.contrib import messages
from django.utils.translation import ngettext
from .utils import send_status_email, send_status_sms  # Import email & SMS functions
from .models import AadhaarDatabase

class MigrantWorkerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'aadhaar_number', 'phone_number', 'status')  # ❌ Removed 'is_approved'
    search_fields = ('full_name', 'aadhaar_number', 'phone_number')
    list_filter = ('status',)

admin.site.register(MigrantWorker, MigrantWorkerAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "status", "updated_by", "submitted_at")
    list_filter = ("status",)
    search_fields = ("name", "email", "phone")
    actions = ["approve_selected", "reject_selected"]

    def save_model(self, request, obj, form, change):
        if change:  # If updating an existing record
            obj.updated_by = request.user  # Track who updated the status
        super().save_model(request, obj, form, change)

    @admin.action(description="Approve selected applications")
    def approve_selected(self, request, queryset):
        updated_count = 0
        for app in queryset:
            if app.status != "Approved":
                app.status = "Approved"
                app.updated_by = request.user
                app.save()
                send_status_email(app)
                send_status_sms(app)
                updated_count += 1
        
        self.message_user(
            request,
            ngettext(
                "%d application was successfully approved.",
                "%d applications were successfully approved.",
                updated_count,
            ) % updated_count,
            messages.SUCCESS,
        )

    @admin.action(description="Reject selected applications")
    def reject_selected(self, request, queryset):
        updated_count = 0
        for app in queryset:
            if app.status != "Rejected":
                app.status = "Rejected"
                app.updated_by = request.user
                app.save()
                send_status_email(app)
                send_status_sms(app)
                updated_count += 1
        
        self.message_user(
            request,
            ngettext(
                "%d application was successfully rejected.",
                "%d applications were successfully rejected.",
                updated_count,
            ) % updated_count,
            messages.ERROR,
        )

admin.site.register(Application, ApplicationAdmin)

@admin.register(AadhaarDatabase)
class AadhaarDatabaseAdmin(admin.ModelAdmin):
    list_display = ("full_name", "aadhaar_number", "date_of_birth", "address")
    search_fields = ("full_name", "aadhaar_number")
    