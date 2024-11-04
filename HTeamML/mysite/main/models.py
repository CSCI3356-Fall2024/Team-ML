from django.db import models
from django.utils import timezone
from django.db.models import Sum

class User(models.Model):
    gradYearOptions = [(2025, "2025"), (2026, "2026"), (2027, "2027"), (2028, "2028"),]

    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255, blank=False, null=False)
    school = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False)
    major = models.CharField(max_length=255, blank=False, null=False)
    minor = models.CharField(max_length=255, blank=True)
    gradyear = models.PositiveIntegerField(choices = gradYearOptions, blank=False, null=False)
    current_points = models.PositiveIntegerField(default=0, null=False)
    total_points = models.PositiveIntegerField(default=0, null=False)
    profile_completed = models.BooleanField(default=False)
    supervisor = models.BooleanField(default=False)
    completed_campaigns = models.ManyToManyField('Campaign', related_name='users', blank=True)
    
    def update_points(self):
        self.total_points = self.completed_campaigns.aggregate(total=Sum('pointsreward'))['total'] or 0
        # Temp current_points
        self.current_points = self.total_points

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
    
    
    
class Campaign(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 255, blank=False, null=False)
    startdate = models.DateField(blank=False, null=False)
    enddate = models.DateField(blank=False, null=False)
    pointsreward = models.PositiveIntegerField(default=0, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    validationmethod = models.CharField(max_length= 255, blank=False)

    @property
    def expired(self):
        return timezone.now().date() > self.enddate
    
    def __str__(self):
        return self.name