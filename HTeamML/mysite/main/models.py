from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255, blank=False, null=False)
    school = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False)
    major = models.CharField(max_length=255, blank=False, null=False)
    minor = models.CharField(max_length=255, default="None", blank=False, null=False)
    gradyear = models.PositiveIntegerField()
    profile_completed = models.BooleanField(default=False)
    supervisor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email

