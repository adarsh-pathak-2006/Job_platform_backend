from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from recruiter.models import Recruitment
from recruiter.serializers import RecruitmentSerializer
from job.throttling import GeneralThrottle, RecruitmentPostingThrottle
from job.permissions import IsRecruiterAndCandidate, IsCandidate, IsRecruiter

class RecruitmentActiveAPI(ListAPIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    serializer_class=RecruitmentSerializer
    def get_queryset(self):
        return Recruitment.objects.filter(is_active=True)

class RecruitmentAllAPI(ListCreateAPIView):
    def get_throttles(self):
        if self.request.method=='POST':
            return [RecruitmentPostingThrottle()]
        return [GeneralThrottle()]

    permission_classes=[IsRecruiter]
        
    serializer_class=RecruitmentSerializer
    queryset=Recruitment.objects.all()

class RecruitmentUpdateAPI(RetrieveUpdateDestroyAPIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='PUT' or self.request.method=='PATCH':
            return [IsRecruiter()]
        elif self.request.method=='DELETE':
            return [IsRecruiter()]
        return [IsRecruiterAndCandidate()]
    serializer_class=RecruitmentSerializer
    queryset=Recruitment.objects.all()

