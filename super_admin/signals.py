from django import dispatch
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.dispatch.dispatcher import Signal
from graduates.models import AcademicHistory, Student
from .models import ActivityLog
import inspect
from accounts.models import RegistrarAdmin, RegistrarStaff
from .utils import get_client_ip


#signaling student registy
@receiver(post_save, sender=Student, dispatch_uid="my_unique_identifier")
def student_registry(sender, instance, created, **kwargs): 
    if created:
        for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
            else:
                request=None 
            
            
        univ= RegistrarStaff.objects.get(user=request.user).university
        print(instance.institution)
        ActivityLog.objects.create(
            user = request.user,
             institution=univ,
            instance=instance,
            operation="student_registry",
            ip_address=get_client_ip(request)


            )

# signal for academic upload

@receiver(post_save, sender=AcademicHistory, dispatch_uid="my_unique_identifier")
def academic_upload(sender, instance, created, **kwargs): 
    if created:
        for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
            else:
                request=None 
            
            
        univ= RegistrarStaff.objects.get(user=request.user).university
        ActivityLog.objects.create(
            user = request.user,
             institution=univ,
            instance=instance,
            operation="academic_upload",
            ip_address=get_client_ip(request)


            )
#signaling student deletion
@receiver(post_delete, sender=Student)
def student_deletion(sender, instance, **kwargs):
    for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
            else:
                request=None 
    univ= RegistrarStaff.objects.get(user=request.user).university
    ActivityLog.objects.create(
            user = request.user,
            institution=univ,
            instance=instance,
            operation="student_deletion",
            ip_address=get_client_ip(request)


          )
#signaling student deletion
@receiver(post_delete, sender=AcademicHistory)
def academic_status_deletion(sender, instance, **kwargs):
    for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
            else:
                request=None 
    univ= RegistrarStaff.objects.get(user=request.user).university
    ActivityLog.objects.create(
            user = request.user,
            institution=univ,
            instance=instance,
            operation="acadmic_status_deletion",
            ip_address=get_client_ip(request)


          )
#signaling registrar staff creation/registration
@receiver(post_save, sender=RegistrarStaff)
def create_staff(sender, instance, created, **kwargs):
    if created:
        for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
            else:
                request=None 
        univ= RegistrarAdmin.objects.get(user=request.user).university
        ActivityLog.objects.create(
            user = request.user,
            institution=univ,
            instance=instance,
            operation="create_staff",
            ip_address=get_client_ip(request)


            )




# custom signal for certificate generations
certificate_generated_signal = Signal(providing_args=['instance', 'request'])

#custom signal for certificates generations
certificates_generated_signal = Signal(providing_args=['instances', 'request'])

#reciever function
@receiver(certificate_generated_signal)
def certificate(sender, instance, request, **kwargs):
    univ= RegistrarStaff.objects.get(user=request.user).university
    ActivityLog.objects.create(
            user = request.user,
            institution=univ,
            instance=instance,
            operation="certificate_generation",
            ip_address=get_client_ip(request)
          )

#custom signal for certificates generations
certificates_generated_signal = Signal(providing_args=['instances', 'request'])

@receiver(certificates_generated_signal)
def certificates(sender, instances, request, **kwargs):
    for instance in instances:
        ActivityLog.objects.create(
            user = request.user,
            instance=instance,
            operation="certificate_generation",
            ip_address=get_client_ip(request)
          )

    




     


    