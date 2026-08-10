from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from authentication.models import User, Company, RecruiterProfile, UserProfile, Resume, Experience, Project

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'mobile_no']

class RegisterSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email', 'mobile_no', 'password']

class UserProfileGetSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=UserProfile
        fields='__all__'

class UserProfileWriteSerializer(ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'
        read_only_fields=['user']

class CompanySerializer(ModelSerializer):
    class Meta:
        model=Company
        fields='__all__'

class RecruiterProfileGetSerializer(ModelSerializer):
    company=CompanySerializer(read_only=True)
    user=UserSerializer(read_only=True)
    class Meta:
        model=RecruiterProfile
        fields='__all__'

class RecruiterProfileWriteSerializer(ModelSerializer):
    company=PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model=RecruiterProfile
        fields='__all__'
        read_only_fields=['user']

class ResumeSerializer(ModelSerializer):
    profile=UserProfileGetSerializer(read_only=True)
    class Meta:
        model=Resume
        fields='__all__'

class ExperienceSerializer(ModelSerializer):
    resume=ResumeSerializer(read_only=True)
    class Meta:
        model=Experience
        fields='__all__'

class ProjectSerializer(ModelSerializer):
    resume=ResumeSerializer(read_only=True)
    class Meta:
        model=Project
        fields='__all__'
