from rest_framework import serializers
from .models import Job, JobApplication
from users.serializers import SkillSerializer, TechStackSerializer
from users.models import Skill, TechStack

class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')

class JobSerializer(serializers.ModelSerializer):
    recruiter_email = serializers.EmailField(source='recruiter.email', read_only=True)
    required_skills = CreatableSlugRelatedField(many=True, slug_field='name', queryset=Skill.objects.all())
    tech_stack = CreatableSlugRelatedField(many=True, slug_field='name', queryset=TechStack.objects.all())

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['recruiter', 'created_at']

    def create(self, validated_data):
        required_skills = validated_data.pop('required_skills', [])
        tech_stack = validated_data.pop('tech_stack', [])
        
        # The serializer automatically provides the user from the view context if save(recruiter=user) is called
        # But here we need to ensure recruiter is set. The view likely converts 'recruiter' to the user object.
        # Let's check how the view calls save().
        
        job = Job.objects.create(**validated_data)
        
        job.required_skills.set(required_skills)
        job.tech_stack.set(tech_stack)
        return job

class JobApplicationSerializer(serializers.ModelSerializer):
    freelancer_email = serializers.EmailField(source='freelancer.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    recruiter_email = serializers.EmailField(source='job.recruiter.email', read_only=True)
    recruiter = serializers.IntegerField(source='job.recruiter.id', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['freelancer', 'job', 'status', 'applied_at']
