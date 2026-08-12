from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from recruiter.models import Recruitment
from recruiter.serializers import RecruitmentSerializer
from job.throttling import GeneralThrottle, RecruitmentPostingThrottle
from job.permissions import IsRecruiterAndCandidate, IsRecruiter

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

    def perform_create(self, serializer):
        from authentication.models import RecruiterProfile, Company
        from rest_framework.exceptions import ValidationError
        try:
            recruiter = RecruiterProfile.objects.get(user=self.request.user)
        except RecruiterProfile.DoesNotExist:
            # Auto-repair: create a default company and profile
            user = self.request.user
            name = f"{user.first_name} {user.last_name}".strip() or user.username
            company = Company.objects.create(
                name=f"{name}'s Company",
                description="Update your company description in your profile."
            )
            recruiter = RecruiterProfile.objects.create(user=user, company=company)
        serializer.save(profile=recruiter)

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

