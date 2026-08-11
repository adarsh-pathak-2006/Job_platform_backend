from django.urls import path
from recruiter.views import RecruitmentActiveAPI, RecruitmentAllAPI, RecruitmentUpdateAPI

urlpatterns = [
    path('recruitement/active/', RecruitmentActiveAPI.as_view(), name='active_recruitment'),
    path('recruitments/', RecruitmentAllAPI.as_view(), name='recruitments'),
    path('recruitment/<int:pk>/', RecruitmentUpdateAPI.as_view(), name='recruitment_detail'),
]
