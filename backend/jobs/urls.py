from django.urls import path
from .views import JobListCreateView, JobDetailView, ApplyJobView, ApplicationListView, ApplicationStatusView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/<int:pk>/apply/', ApplyJobView.as_view(), name='apply_job'),
    path('applications/', ApplicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/status/', ApplicationStatusView.as_view(), name='update_status'),
]
