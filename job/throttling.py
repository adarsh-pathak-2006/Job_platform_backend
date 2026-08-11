from rest_framework.throttling import UserRateThrottle

class RegisterUserThrottle(UserRateThrottle):
    rate="10/minute"

class TokenCreationThrottle(UserRateThrottle):
    rate="15/minute"

class RefreshTokenCreationThrottle(UserRateThrottle):
    rate="7/minute"

class ApplicationCreationThrottle(UserRateThrottle):
    rate="25/minute"

class RecruitmentPostingThrottle(UserRateThrottle):
    rate="25/minute"

class GeneralThrottle(UserRateThrottle):
    rate="60/minute"