from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from recruiter.models import Recruitment, Company
from authentication.serializers import RecruiterProfileGetSerializer, CompanySerializer

class RecruitmentSerializer(ModelSerializer):
    profile=RecruiterProfileGetSerializer(read_only=True)
    class Meta:
        model=Recruitment
        fields='__all__'
