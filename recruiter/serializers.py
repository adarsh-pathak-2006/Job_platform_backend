from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from recruiter.models import Recruitment, Company
from authentication.serializers import RecruiterProfileGetSerializer, CompanySerializer
from authentication.models import RecruiterProfile

class RecruiterGetSerializer(ModelSerializer):
    profile=RecruiterProfileGetSerializer(read_only=True)
    organisation_name=CompanySerializer(read_only=True)
    class Meta:
        model=Recruitment
        fields='__all__'

class RecruiterWriteSerializer(ModelSerializer):
    profile=PrimaryKeyRelatedField(queryset=RecruiterProfile.objects.all())
    organisation_name=PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model=Recruitment
        fields='__all__'