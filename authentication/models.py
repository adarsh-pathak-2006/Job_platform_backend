from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES=[('CANDIDATE', 'Candidate'), ('RECRUITER', 'Recruiter')]

    role=models.CharField(max_length=10, choices=ROLE_CHOICES)
    mobile_no=models.CharField(max_length=15, unique=True)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    display_name=models.CharField()
    bio=models.TextField(blank=True, null=True)
    gender=models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], blank=True, null=True)

    def save(self,*args, **kwargs):
        self.display_name=f"{self.user.first_name} {self.user.last_name}"
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.display_name} - {self.user.role}"

class Resume(models.Model):
    resume_name=models.CharField(max_length=100)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='resumes')
    name=models.CharField(max_length=100)
    gender=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')])
    summary=models.TextField()
    education=models.TextField()
    linkedin=models.URLField(blank=True, null=True)
    github=models.CharField(blank=True, null=True)
    twitter=models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.resume_name} of {self.profile.display_name}"

class Experience(models.Model):
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    organisation_name=models.CharField(max_length=300)
    experience_type=models.CharField(max_length=10, choices=[('INTERNSHIP', 'Internship'), ('PART-TIME', 'Part-Time'), ('FULL-TIME', 'Full-Time')])
    description=models.TextField(blank=True, null=True)
    started_on=models.DateField()
    ended_on=models.DateField()

    def __str__(self):
        return f"{self.organisation_name} added in {self.resume.resume_name}"

    
class Project(models.Model):
    resume=models.ForeignKey(Resume, on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    description=models.TextField()
    live_link=models.URLField(null=True)
    github_link=models.URLField(null=True)


    def __str__(self):
        return f"{self.name} added in {self.resume.resume_name}"

