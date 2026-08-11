from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User=get_user_model()

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role==User.Recruiter)

class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == User.Candidate)

class IsRecruiterAndCandidate(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role in [User.Candidate, User.Recruiter])
        