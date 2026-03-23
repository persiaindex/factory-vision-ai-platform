from django.db import models


class JobStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"


class SizeStatus(models.TextChoices):
    UNDER = "UNDER", "Under"
    OK = "OK", "OK"
    OVER = "OVER", "Over"
    UNKNOWN = "UNKNOWN", "Unknown"


class InspectionJob(models.Model):
    source_image = models.ImageField(upload_to="inspection_jobs/")
    original_filename = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.PENDING,
    )
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processing_started_at = models.DateTimeField(null=True, blank=True)
    processing_finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"InspectionJob(id={self.id}, status={self.status}, file={self.original_filename})"


class DetectionResult(models.Model):
    job = models.ForeignKey(
        InspectionJob,
        on_delete=models.CASCADE,
        related_name="detections",
    )
    object_name = models.CharField(max_length=100)
    confidence = models.FloatField()
    bbox_x_min = models.FloatField()
    bbox_y_min = models.FloatField()
    bbox_x_max = models.FloatField()
    bbox_y_max = models.FloatField()
    estimated_width_mm = models.FloatField(null=True, blank=True)
    estimated_height_mm = models.FloatField(null=True, blank=True)
    estimated_scale_mm_per_pixel = models.FloatField(null=True, blank=True)
    size_status = models.CharField(
        max_length=20,
        choices=SizeStatus.choices,
        default=SizeStatus.UNKNOWN,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return (
            f"DetectionResult(job_id={self.job_id}, object={self.object_name}, "
            f"confidence={self.confidence:.3f})"
        )