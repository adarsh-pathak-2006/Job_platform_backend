from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from candidate.models import Application
from candidate.serializers import (
    ApplicationSerializer,
    ApplicationWriteSerializer,
)

from recruiter.models import Recruitment
from authentication.models import UserProfile

from job.throttling import GeneralThrottle, ApplicationCreationThrottle
from job.permissions import (
    IsCandidate,
    IsRecruiterAndCandidate,
    IsRecruiter,
)


class ApplicationListAPI(APIView):
    throttle_classes = [GeneralThrottle]
    permission_classes = [IsRecruiterAndCandidate]

    def get(self, request, pk):
        job = get_object_or_404(Recruitment, id=pk)

        cache_key = f"applicationsJob_{pk}"
        cache_data = cache.get(cache_key)

        if cache_data is not None:
            return Response(cache_data)

        applications = Application.objects.filter(job=job)
        data = ApplicationSerializer(applications, many=True).data

        cache.set(cache_key, data, timeout=300)

        return Response(data)


class ApplicationUserAPI(APIView):
    throttle_classes = [GeneralThrottle]
    permission_classes = [IsCandidate]

    def get(self, request):
        profile = get_object_or_404(
            UserProfile,
            user=request.user
        )

        cache_key = f"applicationUser_{profile.id}"
        cache_data = cache.get(cache_key)

        if cache_data is not None:
            return Response(cache_data)

        applications = Application.objects.filter(user=profile)
        data = ApplicationSerializer(applications, many=True).data

        cache.set(cache_key, data, timeout=300)

        return Response(data)


class ApplicationCreateAPI(CreateAPIView):
    throttle_classes = [ApplicationCreationThrottle]
    permission_classes = [IsCandidate]
    serializer_class = ApplicationWriteSerializer
    queryset = Application.objects.all()

    def perform_create(self, serializer):
        profile = get_object_or_404(
            UserProfile,
            user=self.request.user
        )
        try:
            application = serializer.save(user=profile)
        except IntegrityError:
            raise ValidationError({'detail': 'You have already applied for this job.'})

        # Candidate's application list is now outdated
        cache.delete(
            f"applicationUser_{profile.id}"
        )

        # Job's application list is now outdated
        cache.delete(
            f"applicationsJob_{application.job_id}"
        )


class ApplicationUserDetailAPI(APIView):
    throttle_classes = [GeneralThrottle]
    permission_classes = [IsCandidate]

    def get(self, request, pk):
        profile = get_object_or_404(
            UserProfile,
            user=request.user
        )

        cache_key = f"applicationsUserDetail_{pk}"
        cache_data = cache.get(cache_key)

        if cache_data is not None:
            return Response(cache_data)

        application = get_object_or_404(
            Application,
            id=pk,
            user=profile
        )

        data = ApplicationSerializer(application).data

        cache.set(cache_key, data, timeout=300)

        return Response(data)

    def delete(self, request, pk):
        profile = get_object_or_404(
            UserProfile,
            user=request.user
        )

        application = get_object_or_404(
            Application,
            id=pk,
            user=profile
        )

        # Save IDs before deleting the object
        job_id = application.job_id
        application_id = application.id

        # Delete every cache that contains this application
        cache.delete(
            f"applicationsUserDetail_{application_id}"
        )

        cache.delete(
            f"applicationsJobDetail_{application_id}_{job_id}"
        )

        cache.delete(
            f"applicationsJob_{job_id}"
        )

        cache.delete(
            f"applicationUser_{profile.id}"
        )

        application.delete()

        return Response(status=204)


class ApplicationJobDetailAPI(APIView):
    throttle_classes = [GeneralThrottle]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsRecruiter()]
        return [IsRecruiter()]

    def get(self, request, pk, ck):
        job = get_object_or_404(
            Recruitment,
            id=ck
        )

        cache_key = f"applicationsJobDetail_{pk}_{ck}"
        cache_data = cache.get(cache_key)

        if cache_data is not None:
            return Response(cache_data)

        application = get_object_or_404(
            Application,
            id=pk,
            job=job
        )

        data = ApplicationSerializer(application).data

        cache.set(cache_key, data, timeout=300)

        return Response(data)

    def delete(self, request, pk, ck):
        job = get_object_or_404(
            Recruitment,
            id=ck
        )

        application = get_object_or_404(
            Application,
            id=pk,
            job=job
        )

        profile = get_object_or_404(
            UserProfile,
            user=application.user.user
        )

        application_id = application.id
        job_id = application.job_id
        user_id = application.user_id

        # Delete all caches affected by this application
        cache.delete(
            f"applicationsJobDetail_{application_id}_{job_id}"
        )

        cache.delete(
            f"applicationsUserDetail_{application_id}"
        )

        cache.delete(
            f"applicationsJob_{job_id}"
        )

        cache.delete(
            f"applicationUser_{user_id}"
        )

        application.delete()

        return Response(status=204)