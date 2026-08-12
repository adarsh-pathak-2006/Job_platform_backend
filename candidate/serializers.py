from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from candidate.models import Application
from authentication.serializers import UserProfileGetSerializer
from recruiter.serializers import RecruitmentSerializer
from recruiter.models import Recruitment

class ApplicationSerializer(ModelSerializer):
    user=UserProfileGetSerializer(read_only=True)
    job=RecruitmentSerializer(read_only=True)
    class Meta:
        model=Application
        fields='__all__'

class ApplicationWriteSerializer(ModelSerializer):
    job=PrimaryKeyRelatedField(queryset=Recruitment.objects.all())
    class Meta:
        model=Application
        fields='__all__'
        read_only_fields=['user', 'resume']
