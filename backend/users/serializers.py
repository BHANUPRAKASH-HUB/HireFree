from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FreelancerProfile, RecruiterProfile, Skill, TechStack

User = get_user_model()

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['id', 'name']

class FreelancerProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Skill.objects.all())
    tech_stack = serializers.SlugRelatedField(many=True, slug_field='name', queryset=TechStack.objects.all())

    class Meta:
        model = FreelancerProfile
        fields = ['bio', 'education', 'experience', 'years_of_experience', 'hourly_rate', 
                 'skills', 'tech_stack', 'linkedin_url', 'portfolio_url', 'resume', 'profile_image']

class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'company_website', 'bio', 'company_logo']

class UserSerializer(serializers.ModelSerializer):
    freelancer_profile = FreelancerProfileSerializer(read_only=True)
    recruiter_profile = RecruiterProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'freelancer_profile', 'recruiter_profile']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        if user.user_type == 'freelancer':
            FreelancerProfile.objects.create(user=user)
        elif user.user_type == 'recruiter':
            RecruiterProfile.objects.create(user=user)
        return user
