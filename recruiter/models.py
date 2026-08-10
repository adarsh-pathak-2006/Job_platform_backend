from django.db import models
from authentication.models import RecruiterProfile, Company

class Recruitment(models.Model):
    profile=models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    organisation_name=models.ForeignKey(Company, on_delete=models.CASCADE)
    employment_type=models.CharField(max_length=10, choices=[('INTERNSHIP', 'Internship'), ('PART-TIME', 'Part-Time'), ('FULL-TIME', 'Full-Time')])
    job_description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.organisation_name.name

