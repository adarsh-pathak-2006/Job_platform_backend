from django.urls import path
from candidate.views import ApplicationListAPI, ApplicationCreateAPI, ApplicationDetailAPI

urlpatterns = [
    path('application/', ApplicationListAPI.as_view(), name='applications'),
    path('application-create/', ApplicationCreateAPI.as_view(), name='application_create'),
    path('application/<int:pk>/', ApplicationDetailAPI.as_view(), name='application_detail')
]
