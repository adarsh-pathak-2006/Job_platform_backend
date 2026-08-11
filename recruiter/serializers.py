from rest_framework.serializers import ModelSerializer
from recruiter.models import Recruitment
from authentication.serializers import RecruiterProfileGetSerializer

class RecruitmentSerializer(ModelSerializer):
    profile=RecruiterProfileGetSerializer(read_only=True)
    class Meta:
        model=Recruitment
        fields='__all__'
