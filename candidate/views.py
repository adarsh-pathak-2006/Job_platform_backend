from django.shortcuts import get_object_or_404
from candidate.models import Application
from candidate.serializers import ApplicationSerializer, ApplicationWriteSerializer
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from job.throttling import GeneralThrottle, ApplicationCreationThrottle
from job.permissions import IsCandidate, IsRecruiterAndCandidate, IsRecruiter
from django.core.cache import cache
from rest_framework.response import Response
from recruiter.models import Recruitment
from authentication.models import UserProfile

class ApplicationListAPI(APIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    def get(self, request, pk):
        cache_data=cache.get(f"applicationsjob_{pk}")
        if cache_data is not None:
            return Response(cache_data, status=200)
        data=Application.objects.filter(job=get_object_or_404(Recruitment, id=pk))
        serial=ApplicationSerializer(data, many=True)
        cache.set(f"applicationsjob_{pk}", serial.data, timeout=300)
        return Response(serial.data, status=200)

class ApplicationUserAPI(APIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    def get(self, request):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        profile_id=profile_data.id
        cache_data=cache.get(f"applicationUser_{profile_id}")
        if cache_data is not None:
            return Response(cache_data, status=200)
        data=Application.objects.filter(user=profile_data)
        serial=ApplicationSerializer(data, many=True)
        cache.set(f"applicationUser_{profile_id}", serial.data, timeout=300)
        return Response(serial.data, status=200)

class ApplicationCreateAPI(CreateAPIView):
    throttle_classes=[ApplicationCreationThrottle]
    permission_classes=[IsCandidate]
    serializer_class=ApplicationWriteSerializer
    queryset=Application.objects.all()

    def perform_create(self, serializer):
        profile_data=get_object_or_404(UserProfile, user=self.request.user)
        application = serializer.save(user=profile_data)
        cache.delete(f"applicationUser_{profile_data.id}")
        cache.delete(f"applicationsJob_{application.job_id}")

class ApplicationUserDetailAPI(APIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='GET':
            return [IsRecruiterAndCandidate()]
        return [IsCandidate()]
    def get(self, request, pk):
        cache_data=cache.get(f"applicationsUserDetail_{pk}")
        if cache_data is not None:
            return Response(cache_data, status=200)
        profile_data=get_object_or_404(UserProfile, user=request.user)
        data=get_object_or_404(Application, id=pk, user=profile_data)
        serial=ApplicationSerializer(data)
        cache.set(f"applicationsUserDetail_{pk}", serial.data, timeout=300)
        return Response(serial.data, status=200)

    def delete(self, request, pk):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        instance=get_object_or_404(Application, id=pk, user=profile_data)
        cache.delete()
        instance.delete(f"applicationsUserDetail_{pk}")
        return Response(status=204)         

class ApplicationJobDetailAPI(APIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='GET':
            return [IsRecruiter()]
        return [IsCandidate()]
    def get(self, request, pk, ck):
        cache_data=cache.get(f"applicationsJobDetail_{pk}_{ck}")
        if cache_data is not None:
            return Response(cache_data, status=200)
        job_data=get_object_or_404(Recruitment, id=ck)
        data=get_object_or_404(Application, id=pk, job=job_data)
        serial=ApplicationSerializer(data)
        cache.set(f"applicationsJobDetail_{pk}_{ck}", serial.data, timeout=300)
        return Response(serial.data, status=200)

    def delete(self, request, pk, ck):
        job_data=get_object_or_404(Recruitment, id=ck)
        instance=get_object_or_404(Application, id=pk, job=job_data)
        profile=get_object_or_404(UserProfile, user=request.user)
        cache.delete(f"applicationsJobDetail_{pk}_{ck}")
        cache.delete(f"applicationsUserDetail_{pk}")
        cache.delete(f"applicationsJob_{instance.job_id}")
        cache.delete(f"applicationsJobDetail_{instance.id}_{instance.job_id}")
        cache.delete(f"applicationUser_{profile.id}")
        instance.delete()
        return Response(status=204) 