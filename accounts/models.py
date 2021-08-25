from django.db import models
from django.contrib.auth.models import AbstractUser
from super_admin.models import University


class User(AbstractUser):
    is_registrar_admin = models.BooleanField(default=False)
    is_registrar_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to="user/", blank=True, null=True, default='user.png')


class RegistrarAdmin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    university= models.OneToOneField(University, on_delete=models.CASCADE, null=True)
    

    

    def __str__(self):
        return str(self.user)

class RegistrarStaff(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=20)
    
    
    def __str__(self):
       return str(self.user)


