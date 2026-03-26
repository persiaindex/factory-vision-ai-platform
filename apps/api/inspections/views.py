from __future__ import annotations

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DetectionResult, InspectionJob, JobStatus
from .serializers import InspectionJobSerializer
from .services import InferenceServiceError, call_inference_service


class InspectionUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")
        if uploaded_file is None:
            return Response(
                {"detail": "No file was uploaded. Use form field name 'file'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job = InspectionJob.objects.create(
            source_image=uploaded_file,
            original_filename=uploaded_file.name,
            status=JobStatus.PENDING,
        )

        try:
            job.status = JobStatus.PROCESSING
            job.processing_started_at = timezone.now()
            job.save(update_fields=["status", "processing_started_at", "updated_at"])

            inference_result = call_inference_service(job.source_image.path)

            for detection in inference_result.get("detections", []):
                DetectionResult.objects.create(
                    job=job,
                    object_name=detection["object_name"],
                    confidence=detection["confidence"],
                    bbox_x_min=detection["bbox_x_min"],
                    bbox_y_min=detection["bbox_y_min"],
                    bbox_x_max=detection["bbox_x_max"],
                    bbox_y_max=detection["bbox_y_max"],
                    estimated_width_mm=detection.get("estimated_width_mm"),
                    estimated_height_mm=detection.get("estimated_height_mm"),
                    estimated_scale_mm_per_pixel=detection.get("estimated_scale_mm_per_pixel"),
                    size_status=detection.get("size_status", "UNKNOWN"),
                )

            job.status = JobStatus.COMPLETED
            job.processing_finished_at = timezone.now()
            job.error_message = ""
            job.save(update_fields=["status", "processing_finished_at", "error_message", "updated_at"])

        except InferenceServiceError as exc:
            job.status = JobStatus.FAILED
            job.processing_finished_at = timezone.now()
            job.error_message = str(exc)
            job.save(update_fields=["status", "processing_finished_at", "error_message", "updated_at"])

            return Response(
                {"detail": "Inference service call failed.", "error": str(exc), "job_id": job.id},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        serializer = InspectionJobSerializer(job, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InspectionJobListView(ListAPIView):
    queryset = InspectionJob.objects.prefetch_related("detections").all()
    serializer_class = InspectionJobSerializer


class InspectionJobDetailView(RetrieveAPIView):
    queryset = InspectionJob.objects.prefetch_related("detections").all()
    serializer_class = InspectionJobSerializer