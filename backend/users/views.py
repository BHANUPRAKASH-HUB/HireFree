from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, FreelancerProfileSerializer, RecruiterProfileSerializer
from .models import Skill, TechStack
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class PublicUserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class TalentListView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='freelancer')
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'freelancer_profile__hourly_rate': ['gte', 'lte'],
        'freelancer_profile__years_of_experience': ['gte', 'lte'],
        'freelancer_profile__skills__name': ['exact'],
    }
    search_fields = ['freelancer_profile__bio', 'freelancer_profile__skills__name', 'email']
    ordering_fields = ['freelancer_profile__hourly_rate', 'freelancer_profile__years_of_experience']

class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.user_type == 'freelancer':
            return FreelancerProfileSerializer
        return RecruiterProfileSerializer

    def get_object(self):
        if self.request.user.user_type == 'freelancer':
            return self.request.user.freelancer_profile
        return self.request.user.recruiter_profile

    def update(self, request, *args, **kwargs):
        # Custom update to handle creating Skills/TechStack on the fly if needed
        # For now, using standard implementation which expects existing SlugRelated fields
        # Ideally we should override to get_or_create skills.
        
        # Checking if we need to auto-create skills
        if 'skills' in request.data:
            skill_names = request.data.get('skills', [])
            for name in skill_names:
                Skill.objects.get_or_create(name=name)
        
        if 'tech_stack' in request.data:
            stack_names = request.data.get('tech_stack', [])
            for name in stack_names:
                TechStack.objects.get_or_create(name=name)

        return super().update(request, *args, **kwargs)
