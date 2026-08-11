from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from recruiter.models import Recruitment
from recruiter.serializers import RecruitmentSerializer

class RecruitmentActiveAPI(ListAPIView):
    serializer_class=RecruitmentSerializer
    def get_queryset(self):
        return Recruitment.objects.filter(is_active=True)

class RecruitmentAllAPI(ListCreateAPIView):
    serializer_class=RecruitmentSerializer
    queryset=Recruitment.objects.all()

class RecruitmentUpdateAPI(RetrieveUpdateDestroyAPIView):
    serializer_class=RecruitmentSerializer
    queryset=Recruitment.objects.all()

