from django.db import models
from authentication.models import RecruiterProfile, Company

class Recruitment(models.Model):
    profile=models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='posting_by_recruiter')
    organisation_name=models.CharField()
    employment_type=models.CharField(max_length=10, choices=[('INTERNSHIP', 'Internship'), ('PART-TIME', 'Part-Time'), ('FULL-TIME', 'Full-Time')])
    job_description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.organisation_name=self.profile.company.name
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.organisation_name.name

