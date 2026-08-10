from django.db import models
from authentication.models import UserProfile, Resume
from recruiter.models import Recruitment


class Application(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    job=models.ForeignKey(Recruitment, on_delete=models.CASCADE)
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[models.UniqueConstraint(fields=['user', 'job'], name='unique_application_per_user_per_job')]

    def __str__(self):
        return self.user.display_name
    