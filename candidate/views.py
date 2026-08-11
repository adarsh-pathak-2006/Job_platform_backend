from candidate.models import Application
from candidate.serializers import ApplicationSerializer, ApplicationWriteSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from job.throttling import GeneralThrottle, ApplicationCreationThrottle
from job.permissions import IsCandidate, IsRecruiterAndCandidate

class ApplicationListAPI(ListAPIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    serializer_class=ApplicationSerializer
    queryset=Application.objects.all()

class ApplicationCreateAPI(CreateAPIView):
    throttle_classes=[ApplicationCreationThrottle]
    permission_classes=[IsCandidate]
    serializer_class=ApplicationWriteSerializer
    queryset=Application.objects.all()

class ApplicationDetailAPI(RetrieveDestroyAPIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='GET':
            return [IsRecruiterAndCandidate()]
        return [IsCandidate()]
    serializer_class=ApplicationSerializer
    queryset=Application.objects.all()
