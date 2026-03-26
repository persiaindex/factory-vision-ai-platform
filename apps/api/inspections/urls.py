from django.urls import path

from .views import InspectionJobDetailView, InspectionJobListView, InspectionUploadView

urlpatterns = [
    path("inspections/upload/", InspectionUploadView.as_view(), name="inspection-upload"),
    path("inspections/jobs/", InspectionJobListView.as_view(), name="inspection-job-list"),
    path("inspections/jobs/<int:pk>/", InspectionJobDetailView.as_view(), name="inspection-job-detail"),
]