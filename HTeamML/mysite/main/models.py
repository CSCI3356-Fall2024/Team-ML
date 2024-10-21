from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    major = models.CharField(max_length=255)
    gradyear = models.PositiveIntegerField()
    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname