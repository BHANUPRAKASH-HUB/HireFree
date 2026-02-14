from rest_framework import generics, permissions, status, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from notifications.models import Notification

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_recruiter

class IsFreelancer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_freelancer

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'job_type': ['exact'],
        'experience_level': ['exact'],
        'pay_per_hour': ['gte', 'lte'],
        'required_skills__name': ['exact'],
        'location': ['iexact'],
    }
    search_fields = ['title', 'description', 'required_skills__name', 'tech_stack__name']
    ordering_fields = ['created_at', 'pay_per_hour', 'experience_level']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsRecruiter()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UpdateApplicationStatusView(generics.UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplyJobView(APIView):
    permission_classes = [IsFreelancer]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        if JobApplication.objects.filter(job=job, freelancer=request.user).exists():
            return Response({"message": "Already applied"}, status=status.HTTP_400_BAD_REQUEST)
        
        application = JobApplication.objects.create(
            job=job, 
            freelancer=request.user,
            cover_letter=request.data.get('cover_letter', '')
        )
        
        # Notify Recruiter
        Notification.objects.create(
            recipient=job.recruiter,
            title="New Application",
            message=f"{request.user.email} applied for {job.title}"
        )
        
        return Response(JobApplicationSerializer(application).data, status=status.HTTP_201_CREATED)

class ApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'user_type', None) == 'recruiter':
            return JobApplication.objects.filter(job__recruiter=user)
        return JobApplication.objects.filter(freelancer=user)

class ApplicationStatusView(APIView):
    permission_classes = [IsRecruiter]

    def patch(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        if application.job.recruiter != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        status_val = request.data.get('status')
        if status_val in ['accepted', 'rejected']:
            application.status = status_val
            application.save()
            
            # Notify Freelancer
            Notification.objects.create(
                recipient=application.freelancer,
                title=f"Application {status_val.capitalize()}",
                message=f"Your application for {application.job.title} was {status_val}."
            )
            return Response({"status": status_val})
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
