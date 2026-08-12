from django.shortcuts import get_object_or_404
from candidate.models import Application
from candidate.serializers import ApplicationSerializer, ApplicationWriteSerializer
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from job.throttling import GeneralThrottle, ApplicationCreationThrottle
from job.permissions import IsCandidate, IsRecruiterAndCandidate
from django.core.cache import cache
from rest_framework.response import Response

class ApplicationListAPI(APIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    def get(self, request):
        cache_data=cache.get("applications")
        if cache_data is not None:
            return Response(cache_data, status=200)
        data=Application.objects.all()
        serial=ApplicationSerializer(data, many=True)
        cache.set("applications", serial.data, timeout=300)
        return Response(serial.data, status=200)

class ApplicationCreateAPI(CreateAPIView):
    throttle_classes=[ApplicationCreationThrottle]
    permission_classes=[IsCandidate]
    serializer_class=ApplicationWriteSerializer
    queryset=Application.objects.all()

class ApplicationDetailAPI(APIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='GET':
            return [IsRecruiterAndCandidate()]
        return [IsCandidate()]
    def get(self, request, pk):
        cache_data=cache.get(f"applications_{pk}")
        if cache_data is not None:
            return Response(cache_data, status=200)
        data=get_object_or_404(Application, id=pk)
        serial=ApplicationSerializer(data)
        cache.set(f"applications_{pk}", serial.data, timeout=300)
        return Response(serial.data, status=200)

    def put(self, request, pk):
        instance=get_object_or_404(Application, id=pk)
        serial=ApplicationSerializer(instance, data=request.data)
        if serial.is_valid():
            cache.delete(f"applications_{pk}")
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

    def delete(self, request, pk):
        instance=get_object_or_404(Application, id=pk)
        instance.delete()
        return Response(status=204)         
