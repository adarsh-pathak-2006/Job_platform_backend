from django.urls import path
from authentication.views import CompanyAPI, CompanyDetailAPI, UserProfileAPI, UserProfileIndividualAPI, RecruiterProfileAPI, RecruiterProfileIndividualAPI, MyProfile, ResumeAPI, ResumeDetailAPI, ExperienceAPI, ExperienceIndividualAPI, ProjectAPI, ProjectIndividualAPI

urlpatterns = [
    path('company/', CompanyAPI.as_view(), name='company'),
    path('company/<int:pk>/', CompanyDetailAPI.as_view(), name='company_detail'),
    path('candidate-profile/', UserProfileAPI.as_view(), name='user_profiles'),
    path('candiate-profile/<int:pk>/', UserProfileIndividualAPI.as_view(), name='user_profile_individual'),
    path('recruiter-profile/', RecruiterProfileAPI.as_view(), name='recruiter_profiles'),
    path('recruiter-profile/<int:pk>/', RecruiterProfileIndividualAPI.as_view(), name='recruiter_profile_individual'),
    path('my-profile/', MyProfile.as_view(), name='my_profile'),
    path('resume/', ResumeAPI.as_view(), name='resume'),
    path('resume/<int:pk>/', ResumeDetailAPI.as_view(), name='resume_individual'),
    path('experience/<int:pk>/', ExperienceAPI.as_view(), name='experience'),
    path('experience/<int:pk>/<int:ck>/', ExperienceIndividualAPI.as_view(), name='experience_individual'),
    path('project/<int:pk>/', ProjectAPI.as_view(), name='project_api'),
    path('project/<int:pk>/<int:ck>/', ProjectIndividualAPI.as_view(), name='project_individual'),
]
