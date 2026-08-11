from candidate.models import Application
from candidate.serializers import ApplicationSerializer, ApplicationWriteSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView


class ApplicationListAPI(ListAPIView):
    serializer_class=ApplicationSerializer
    queryset=Application.objects.all()

class ApplicationCreateAPI(CreateAPIView):
    serializer_class=ApplicationWriteSerializer
    queryset=Application.objects.all()

class ApplicationDetailAPI(RetrieveDestroyAPIView):
    serializer_class=ApplicationSerializer
    queryset=Application.objects.all()
