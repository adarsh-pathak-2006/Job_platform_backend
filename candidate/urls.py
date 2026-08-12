from django.urls import path

from candidate.views import (
    ApplicationListAPI,
    ApplicationCreateAPI,
    ApplicationUserAPI,
    ApplicationUserDetailAPI,
    ApplicationJobDetailAPI,
)


urlpatterns = [

    # Candidate's applications
    path(
        "application/user/",
        ApplicationUserAPI.as_view(),
        name="application_user",
    ),

    # Applications belonging to a particular job
    path(
        "application/job/<int:pk>/",
        ApplicationListAPI.as_view(),
        name="application_job_list",
    ),

    # Create application
    path(
        "application/create/",
        ApplicationCreateAPI.as_view(),
        name="application_create",
    ),

    # Candidate application detail/delete
    path(
        "application/<int:pk>/",
        ApplicationUserDetailAPI.as_view(),
        name="application_user_detail",
    ),

    # Recruiter application detail/delete
    path(
        "application/job/<int:ck>/<int:pk>/",
        ApplicationJobDetailAPI.as_view(),
        name="application_job_detail",
    ),
]