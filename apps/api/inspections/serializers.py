from rest_framework import serializers

from .models import DetectionResult, InspectionJob


class DetectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionResult
        fields = [
            "id",
            "object_name",
            "confidence",
            "bbox_x_min",
            "bbox_y_min",
            "bbox_x_max",
            "bbox_y_max",
            "estimated_width_mm",
            "estimated_height_mm",
            "estimated_scale_mm_per_pixel",
            "size_status",
            "created_at",
        ]


class InspectionJobSerializer(serializers.ModelSerializer):
    detections = DetectionResultSerializer(many=True, read_only=True)
    source_image_url = serializers.SerializerMethodField()
    source_image_proxy_url = serializers.SerializerMethodField()

    class Meta:
        model = InspectionJob
        fields = [
            "id",
            "original_filename",
            "source_image",
            "source_image_url",
            "source_image_proxy_url",
            "status",
            "error_message",
            "created_at",
            "updated_at",
            "processing_started_at",
            "processing_finished_at",
            "detections",
        ]

    def get_source_image_url(self, obj):
        if not obj.source_image:
            return None
        return obj.source_image.url

    def get_source_image_proxy_url(self, obj):
        if not obj.source_image:
            return None
        return f"/backend{obj.source_image.url}"