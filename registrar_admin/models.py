from django.db import models
from super_admin.models import University
from django.conf import settings
from accounts.models import RegistrarAdmin
User = settings.AUTH_USER_MODEL

from .validators import validate_even




class Faculty(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    total_programs = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('university', 'name',)
        ordering = ['-id']

    def __str__(self):
        return self.name

  


class Program(models.Model):
    degree_type =(
        (
           'BA','Bachelor of  Art',
        ),
        (
            'BSc','Bachelor of Science'
        ),
        (
           'BEd','Bachelor of Science'
        ),
        (
            'MD','Master of Doctorate'
        ),
        (
            'BPH', 'Bachelor of Pharmacy'
        ),

    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    year_required = models.PositiveSmallIntegerField(validators=[validate_even])
    degree_type = models.CharField(max_length=50, choices=degree_type)

    def __str__(self):
        return self.name


# request db

class Request(models.Model):
    request_status =(
        ('pending','pending'),
        ('approved','approved'),
        ('expired','expired'),
    )
    sender = models.ForeignKey(RegistrarAdmin, on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.TextField()
    status = models.CharField(max_length=50, choices=request_status, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.request
    