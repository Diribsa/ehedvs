from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
User = settings.AUTH_USER_MODEL


#university db
class University(models.Model):
    name = models.CharField(max_length=300, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_no1 = PhoneNumberField(unique=True)
    phone_no2 = PhoneNumberField(blank=True, null=True, unique=True)
    fax_no = PhoneNumberField(unique=True)
    website = models.URLField(max_length=200, unique=True)
    pob = models.PositiveSmallIntegerField(unique=True)
    city = models.CharField(max_length=200, blank=True,)
    logo = models.ImageField(upload_to="logos/")

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


# activitylog tracer 
class ActivityLog(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    institution = models.ForeignKey(University, blank=True, null=True, on_delete=models.SET_NULL)
    instance = models.CharField(max_length=250)
    operation = models.CharField(max_length=100, editable=False)
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.operation == "student_registry":
            return "%s Registered  %s on %s" % (self.user, self.instance, self.timestamp)
        elif self.operation == "student_deletion":
            return "%s Deleted %s on %s" % (self.user, self.instance, self.timestamp)
        elif self.operation == "create_staff":
            return "%s Created account for %s on %s" % (self.user, self.instance, self.timestamp)

        elif self.operation == "certificate_generation":
            return " Certificate of %s  generated on %s by %s" % (self.instance, self.timestamp, self.user)

        elif self.operation == "academic_upload":
            return " Academic status of %s  uploaded on %s by %s" % (self.instance, self.timestamp, self.user)
        elif self.operation == "acadmic_status_deletion":
            return " Academic status of %s  deleted on %s by %s" % (self.instance, self.timestamp, self.user)

    class Meta:
        ordering = ['-timestamp']


    




