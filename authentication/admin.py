from django.contrib import admin
from authentication.models import Resume, Profile, User, Project, Experience

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(User)
admin.site.register(Profile)
