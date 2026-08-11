from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from authentication.models import Company, RecruiterProfile, UserProfile, Resume, Experience, Project
from authentication.serializers import RegisterSerializer, UserProfileWriteSerializer, UserProfileGetSerializer, CompanySerializer, RecruiterProfileGetSerializer, RecruiterProfileWriteSerializer, ResumeSerializer, ExperienceSerializer, ProjectSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView

User=get_user_model()

class RegisterAPI(APIView):
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            f_name=serial.validated_data['first_name']
            l_name=serial.validated_data['l_name']
            email=serial.validated_data['email']
            mobile_no=serial.validated_data['mobile_no']
            password=serial.validated_data['password']
            role=serial.validated_data['role']

            if User.objects.filter(Q(username=username) | Q(email=email) | Q(mobile_no=mobile_no)):
                return Response({'message':'username or email or mobile_no already exists'}, status=400)
            user=User.objects.create_user(username=username, mobile_no=mobile_no, email=email, password=password, role=role, first_name=f_name, last_name=l_name)
            if role=='Candidate':
                UserProfile.objects.create(user=user)
            elif role=='Recruiter':
                RecruiterProfile.objects.create(user=user)
            return Response({'message':'user registered'}, status=201)
        return Response(serial.errors, status=400)

class CompanyAPI(ListCreateAPIView):
    serializer_class=CompanySerializer
    queryset=Company.objects.all()

class CompanyDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class=CompanySerializer
    queryset=Company.objects.all()

class UserProfileAPI(ListAPIView):
    serializer_class=UserProfileGetSerializer
    queryset=UserProfile.objects.all()

class UserProfileIndividualAPI(RetrieveAPIView):
    serializer_class=UserProfileGetSerializer
    queryset=UserProfile.objects.all()

class RecruiterProfileAPI(ListAPIView):
    serializer_class=RecruiterProfileGetSerializer
    queryset=RecruiterProfile.objects.all()

class RecruiterProfileIndividualAPI(RetrieveAPIView):
    serializer_class=RecruiterProfileGetSerializer
    queryset=RecruiterProfile.objects.all()

class MyProfile(RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.user.role=='Candidate':
            return UserProfileWriteSerializer
        elif self.request.user.role=='Recruiter':
            return RecruiterProfileWriteSerializer  

    def get_object(self):
        if self.request.user.role=='Candidate':
            return get_object_or_404(UserProfile, user=self.request.user)
        elif self.request.user.role=='Recruiter':
            return get_object_or_404(RecruiterProfile, user=self.request.user)       

class ResumeAPI(ListCreateAPIView):
    serializer_class=ResumeSerializer

    def get_queryset(self):
        profile_data=UserProfile.objects.filter(user=self.request.user)
        return Resume.objects.filter(profile=profile_data)

class ResumeDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class=ResumeSerializer
    
    def get_queryset(self):
        profile_data=UserProfile.objects.filter(user=self.request.user)
        return Resume.objects.filter(profile=profile_data)

class ExperienceAPI(APIView):
    def get(self, request, pk):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
        data=Experience.objects.filter(resume=resume_data)
        serial=ExperienceSerializer(data, many=True)
        return Response(serial.data, status=200)

    def post(self, request, pk):
        serial=ExperienceSerializer(data=request.data)
        if serial.is_valid():
            profile_data=get_object_or_404(UserProfile, user=request.user)
            resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
            serial.save(resume=resume_data)
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)

class ExperienceIndividualAPI(APIView):
    def get(self, request, pk, ck):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
        data=get_object_or_404(Experience, resume=resume_data, id=ck)
        serial=ExperienceSerializer(data)
        return Response(serial.data, status=200)

    def put(self, request, pk, ck):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
        instance=get_object_or_404(Experience,resume=resume_data, id=ck)
        serial=ExperienceSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

    def delete(self, request, pk, ck):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
        instance=get_object_or_404(Experience,resume=resume_data, id=ck)
        instance.delete()
        return Response(status=204)

class ProjectAPI(ListCreateAPIView):
    def get(self, request, pk):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
        data=Project.objects.filter(resume=resume_data)
        serial=ProjectSerializer(data, many=True)
        return Response(serial.data, status=200)

    def post(self, request, pk):
        serial=ProjectSerializer(data=request.data)
        if serial.is_valid():
            profile_data=get_object_or_404(UserProfile, user=request.user)
            resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
            serial.save(resume=resume_data)
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)   

class ProjectIndividualAPI(APIView):
    def get(self, request, pk, ck):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
        data=get_object_or_404(Project, resume=resume_data, id=ck)
        serial=ProjectSerializer(data)
        return Response(serial.data, status=200)

    def put(self, request, pk, ck):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
        instance=get_object_or_404(Project,resume=resume_data, id=ck)
        serial=ProjectSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

    def delete(self, request, pk, ck):
        profile_data=get_object_or_404(UserProfile, user=request.user)
        resume_data=get_object_or_404(Resume,profile=profile_data, id=pk)
        instance=get_object_or_404(Project,resume=resume_data, id=ck)
        instance.delete()
        return Response(status=204)                         