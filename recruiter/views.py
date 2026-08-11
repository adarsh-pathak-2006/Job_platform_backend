from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from recruiter.models import Recruitment
from recruiter.serializers import RecruitmentGetSerializer, RecruitmentWriteSerializer

class RecruitmentActiveAPI(ListAPIView):
    serializer_class=RecruitmentGetSerializer
    def get_queryset(self):
        return Recruitment.objects.filter(is_active=True)

class RecruitmentAllAPI(ListAPIView):
    serializer_class=RecruitmentGetSerializer
    queryset=Recruitment.objects.all()

class RecruitmentCreateAPI(CreateAPIView):
    serializer_class=RecruitmentWriteSerializer
    queryset=Recruitment.objects.all()

class RecruitmentUpdateAPI(RetrieveUpdateDestroyAPIView):
    serializer_class=RecruitmentWriteSerializer
    queryset=Recruitment.objects.all()

