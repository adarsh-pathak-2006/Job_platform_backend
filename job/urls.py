"""
URL configuration for job project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authentication.views import RegisterAPI, CustomTokenObtainView, CustomTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('token/', CustomTokenObtainView.as_view(), name='token_obtain_view'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh_view'),
    path('api/auth/', include('authentication.urls')),
    path('api/candidate/', include('candidate.urls')),
    path('api/recruiter/', include('recruiter.urls')),
]
