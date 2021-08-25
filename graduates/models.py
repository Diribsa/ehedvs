from typing import Tuple
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from super_admin.models import University
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from accounts.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from registrar_admin.models import Faculty, Program


#from ehedvs import settings


class Student(models.Model):
    institution = models.ForeignKey(
        University, on_delete=models.CASCADE, null=True)
    id = models.CharField(max_length=200, primary_key=True,
                          verbose_name='ID Number ')
    full_name = models.CharField(max_length=255, verbose_name='student name')
    gender = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    registration_year = models.DateField(
        auto_now_add=True, null=True, verbose_name='Registration_Date')
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        Program, on_delete=models.SET_NULL, null=True, blank=True)
    level_of_completion = models.FloatField(default=0.0, blank=True, null=True)

    class Meta:
        ordering = ['-registration_year']

    def __str__(self):
        return self.full_name


def academic_status_determiner(batch, semester, GPA, CGPA):
    if batch == 1 and semester == 1:
        if GPA >= 1.50 and CGPA >= 1.50:
            status = "Promoted"
        else:
            status = "Dismissed"
    elif batch == 1 and semester == 2:
        if GPA < 1.50 or CGPA < 1.75:
            status = "Dismissed"
        else:
            status = "Promoted"

    elif batch >=2:
        if GPA<1.50 or CGPA < 1.75:
            status = "Dismissed"
        else:
            status = "Promoted"


    
    else:
        status = "Dismissed"

    return status


class AcademicHistory(models.Model):
    sem = (
        ('1', '1st semester'),
        ('2', '2nd semester'),
    )
    status = (
        ('Promoted', 'Promoted'),
        ('Dismissed', 'Dismissed'),
        ('suspended', 'suspended')
    )
    batch = (
        ('1', '1st year'),
        ('2', '2nd year'),
        ('3', '3rd year'),
        ('4', '4th year'),
        ('5', '5th year'),
        ('6', '6th year'),
    )

    student = models.ForeignKey(Student,  on_delete=models.CASCADE)
    batch = models.CharField(
        max_length=20, choices=batch, verbose_name="Class Year")
    semester = models.CharField(max_length=20, choices=sem)
    GPA = models.FloatField(default=0.0)
    CGPA = models.FloatField(default=0.0)
    academic_status = models.CharField(
        max_length=20, choices=status, blank=True, null=True)
    uploaded_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True)
    uploaded_date = models.DateField(auto_now=True, verbose_name='Date')

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return "%s 's  %s year %s semester Academical status " % (self.student, self.batch, self.semester)


@receiver(pre_save, sender=AcademicHistory)
def accademical_status(sender, instance, *args, **kwargs):
    instance.academic_status = academic_status_determiner(
        instance.batch, instance.semester, instance.GPA, instance.CGPA)


class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes')
    image = models.ImageField(default='default.png', upload_to='student_image')

    def __str__(self):
        return f'{self.student} Profile'


# pre_save signal for generating  qr_code

@receiver(pre_save, sender=Profile)
def profile_pre_save(sender, instance, *args, **kwargs):
    if not instance.qr_code:
        qrcode_img = qrcode.make(instance.student.id)
        canvas = Image.new('RGB', (320, 320), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{instance.student.id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        instance.qr_code.save(fname, File(buffer), save=False)
        canvas.close()



 




