from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from authentication.models import Company, RecruiterProfile, UserProfile, Resume, Experience, Project
from authentication.serializers import RegisterSerializer, UserProfileWriteSerializer, UserProfileGetSerializer, CompanySerializer, RecruiterProfileGetSerializer, RecruiterProfileWriteSerializer, ResumeSerializer, ExperienceSerializer, ProjectSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from job.permissions import IsCandidate, IsRecruiterAndCandidate
from rest_framework.permissions import IsAdminUser
from job.throttling import GeneralThrottle, RegisterUserThrottle, TokenCreationThrottle, RefreshTokenCreationThrottle
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User=get_user_model()

class CustomTokenObtainView(TokenObtainPairView):
    throttle_classes=[TokenCreationThrottle]
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes=[RefreshTokenCreationThrottle]

class RegisterAPI(APIView):
    throttle_classes=[RegisterUserThrottle]
    serializer_class = RegisterSerializer
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            f_name=serial.validated_data.get('first_name', '')
            l_name=serial.validated_data.get('last_name', '')
            email=serial.validated_data['email']
            mobile_no=serial.validated_data['mobile_no']
            password=serial.validated_data['password']
            role=serial.validated_data['role']

            if User.objects.filter(Q(username=username) | Q(email=email) | Q(mobile_no=mobile_no)):
                return Response({'message':'username or email or mobile_no already exists'}, status=400)
            user=User.objects.create_user(username=username, mobile_no=mobile_no, email=email, password=password, role=role, first_name=f_name, last_name=l_name)
            if role.upper() == 'CANDIDATE':
                UserProfile.objects.create(user=user)
            elif role.upper() == 'RECRUITER':
                # Use provided company name or generate a default one
                company_name = request.data.get('company_name', '').strip() or f"{f_name} {l_name}'s Company"
                company = Company.objects.create(
                    name=company_name,
                    description="Update your company description in your profile."
                )
                RecruiterProfile.objects.create(user=user, company=company)
            return Response({'message':'user registered'}, status=201)
        return Response(serial.errors, status=400)

class CompanyAPI(ListCreateAPIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='GET':
            return [IsRecruiterAndCandidate()]
        return [IsAdminUser()]
    serializer_class=CompanySerializer
    queryset=Company.objects.all()

class CompanyDetailAPI(RetrieveUpdateDestroyAPIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='GET':
            return [IsRecruiterAndCandidate()]
        return [IsAdminUser()]
    serializer_class=CompanySerializer
    queryset=Company.objects.all()

class UserProfileAPI(ListAPIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    serializer_class=UserProfileGetSerializer
    queryset=UserProfile.objects.all()

class UserProfileIndividualAPI(RetrieveAPIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    serializer_class=UserProfileGetSerializer
    queryset=UserProfile.objects.all()

class RecruiterProfileAPI(ListAPIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    serializer_class=RecruiterProfileGetSerializer
    queryset=RecruiterProfile.objects.all()

class RecruiterProfileIndividualAPI(RetrieveAPIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    serializer_class=RecruiterProfileGetSerializer
    queryset=RecruiterProfile.objects.all()

class MyProfile(RetrieveUpdateDestroyAPIView):
    throttle_classes=[GeneralThrottle]
    permission_classes=[IsRecruiterAndCandidate]
    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request or not self.request.user.is_authenticated:
            return UserProfileWriteSerializer
        if self.request.user.role == 'CANDIDATE' or self.request.user.role == 'Candidate':
            return UserProfileWriteSerializer
        elif self.request.user.role == 'RECRUITER' or self.request.user.role == 'Recruiter':
            return RecruiterProfileWriteSerializer
        return UserProfileWriteSerializer

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request or not self.request.user.is_authenticated:
            return None
        if self.request.user.role == 'CANDIDATE':
            obj, _ = UserProfile.objects.get_or_create(user=self.request.user)
            return obj
        elif self.request.user.role == 'RECRUITER':
            return get_object_or_404(RecruiterProfile, user=self.request.user)
        return None

class ResumeAPI(ListCreateAPIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='POST':
            return [IsCandidate()]
        return [IsRecruiterAndCandidate()]
    serializer_class=ResumeSerializer

    def get_queryset(self):
        profile_data=UserProfile.objects.filter(user=self.request.user)
        return Resume.objects.filter(profile__in=profile_data)
        
    def perform_create(self, serializer):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        serializer.save(profile=profile)

class ResumeDetailAPI(RetrieveUpdateDestroyAPIView):
    throttle_classes=[GeneralThrottle]
    def get_permissions(self):
        if self.request.method=='PUT' or self.request.method=='DELETE':
            return [IsCandidate()]
        return [IsRecruiterAndCandidate()]
    serializer_class=ResumeSerializer
    
    def get_queryset(self):
        profile_data=UserProfile.objects.filter(user=self.request.user)
        return Resume.objects.filter(profile__in=profile_data)

class ExperienceAPI(APIView):
    throttle_classes=[GeneralThrottle]
    serializer_class = ExperienceSerializer
    def get_permissions(self):
        if self.request.method=='POST':
            return [IsCandidate()]
        return [IsRecruiterAndCandidate()]
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
    throttle_classes=[GeneralThrottle]
    serializer_class = ExperienceSerializer
    def get_permissions(self):
        if self.request.method=='PUT' or self.request.method=='DELETE':
            return [IsCandidate()]
        return [IsRecruiterAndCandidate()]
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
    throttle_classes=[GeneralThrottle]
    serializer_class = ProjectSerializer
    def get_permissions(self):
        if self.request.method=='POST':
            return [IsCandidate()]
        return [IsRecruiterAndCandidate()]
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
    throttle_classes=[GeneralThrottle]
    serializer_class = ProjectSerializer
    def get_permissions(self):
        if self.request.method=='PUT' or self.request.method=='DELETE':
            return [IsCandidate()]
        return [IsRecruiterAndCandidate()]
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