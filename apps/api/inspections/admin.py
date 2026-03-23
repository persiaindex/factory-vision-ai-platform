from django.contrib import admin

from .models import DetectionResult, InspectionJob


class DetectionResultInline(admin.TabularInline):
    model = DetectionResult
    extra = 0


@admin.register(InspectionJob)
class InspectionJobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "original_filename",
        "status",
        "created_at",
        "processing_started_at",
        "processing_finished_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("original_filename", "error_message")
    readonly_fields = ("created_at", "updated_at")
    inlines = [DetectionResultInline]


@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "job",
        "object_name",
        "confidence",
        "size_status",
        "created_at",
    )
    list_filter = ("object_name", "size_status", "created_at")
    search_fields = ("object_name", "job__original_filename")