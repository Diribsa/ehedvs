from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from super_admin.models import University, ActivityLog
from accounts.models import RegistrarAdmin, RegistrarStaff, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import AdminSignUpForm
from django.contrib.auth.decorators import login_required
from .forms import UniversityForm
from accounts.decorators import registrar_admin, registrar_staff, super_admin
from registrar_admin.models import Request, Faculty
from graduates.models import Student
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from background_task import background
from background_task.models import CompletedTask
import subprocess
import shlex






#dashboar on super admin page
@login_required(login_url='accounts:login')
@super_admin
def dashboard(request):
    lists = University.objects.all().order_by('-id')
    total_unv = lists.count()
    registrar_admin = RegistrarAdmin.objects.all().count()
    registrar_staff = RegistrarStaff.objects.all().count()
    users=registrar_admin+registrar_staff
    context = {'lists':lists , 'total_unv':total_unv, 'users':users}
    return render(request, 'super_admin/dashboard.html', context)

# register high educational institution
@login_required(login_url='accounts:login')
@super_admin
def registration(request):
    form = UniversityForm()
    if request.method=='POST':
        form = UniversityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/super_admin/')
    context = {'form':form}
    return render(request, 'super_admin/register.html', context)



#create account for registrar admin
@login_required(login_url='accounts:login')
@super_admin
def createAccount(request):
    form = AdminSignUpForm()
    if request.method=='POST':
        try:
            form = AdminSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                print(request.POST['university'])
                return redirect('/super_admin/user_profile')
            else:
                 messages.warning(request,'the two password doesnot match')
           
 
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                #return redirect('/accounts/exist/')
                messages.warning(request,'University you have selected has got ADIMN already')
               
        
    context = {'form': form}
    return render(request, 'super_admin/account.html', context)

#user profile
@login_required(login_url='accounts:login')
@super_admin
def useProfile(request):
    lists = RegistrarAdmin.objects.all().order_by('-user_id')[:6]
    context = {'lists':lists}
    return render(request, 'super_admin/user_profile.html', context)


#institution detail
def institution_detail(request, id):
    institution = University.objects.get(id=id)
    registrar_staffs = RegistrarStaff.objects.filter(university=institution).count()
    students = Student.objects.filter(institution=institution).count()
    recent_activites = ActivityLog.objects.filter(institution=institution)[:3]
    certificate_generated = ActivityLog.objects.filter(operation="certificate_generation", institution=institution).count()
    
    schools = Faculty.objects.filter(university=institution)[:4]

    try:
        registrar_admin=RegistrarAdmin.objects.get(university=institution)
        registrar_staffs=registrar_staffs+1
    
    except RegistrarAdmin.DoesNotExist:
        registrar_admin="No Admin"
    

    context = {
         'institution':institution,
         'registrar_admin':registrar_admin,
         'registrar_staffs':registrar_staffs,
         'students':students,
         'recent_activites':recent_activites,
         'certificate_generated': certificate_generated,
         'schools':schools
    }
    return render(request, 'super_admin/university.html', context)

#update univeristy
@login_required(login_url='accounts:login')
@super_admin
def updateUnv(request, pk):
    univ = University.objects.get(id=pk)
    form = UniversityForm(instance=univ)
    if request.method=='POST':
        form = UniversityForm(request.POST, instance=univ)
        if form.is_valid():
            form.save()
            return redirect('/super_admin/')
    context = {'form':form}
    return render(request, 'super_admin/register.html', context)

#delete University
@login_required(login_url='accounts:login')
@super_admin
def deleteUnv(request, pk ):
    univ = University.objects.get(id=pk)
    univ.delete()
    return redirect("/super_admin/")

#delet Registrar_admin
@login_required(login_url='accounts:login')
@super_admin
def deleteRegAdmin(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect("/super_admin/user_profile/")

#activity logs
@login_required(login_url='accounts:login')
@super_admin
def activity_logs(request):
    activities = ActivityLog.objects.all()
    user_creation = ActivityLog.objects.filter(operation="create_staff").count()
    student_registry = ActivityLog.objects.filter(operation="student_registry").count()
    certificate_generation = ActivityLog.objects.filter(operation="student_deletion").count()
    student_deletion = ActivityLog.objects.filter(operation="certificate_generation").count()
    context = {

       'activities':activities,
       'user_creation':user_creation,
       'student_registry':student_registry,
       'certificate_generation': certificate_generation,
       'student_deletion':student_deletion,
    }
    return render(request, 'super_admin/activiy_logs.html', context)


# view send request
def view_request(request):
    subjects = Request.objects.all()[0:5]
    context = {
        'subjects':subjects
    }
    return render(request, 'super_admin/view_request.html', context)

#chat with specific user
def message_with_registrar_admin(request, id):
    registrar_admin = RegistrarAdmin.objects.get(user_id=id)
    last_message = Request.objects.filter(sender=registrar_admin).first()
    if request.method =='POST':
        subject = request.POST.get('subject')
        super_admin = get_user_model().objects.get(is_superuser=True)
        Request.objects.create(sender=registrar_admin, reciever=super_admin, request=subject)
    
    
    context = {
     'registrar_admin':registrar_admin,
     'last_message': last_message 
    }
    return render(request, 'super_admin/message_with_ra.html', context)
# approving request
def approve_request(request, id):
    subject = Request.objects.get(id=id)
    if request.method == 'POST':
        Request.objects.filter(id=id).update(status="approved")
        CompletedTask.objects.all().delete()
        process_tasks()
        expire_request(pk=id)
        return redirect('/super_admin/view_request')
    context = {'subject':subject}
    return render(request, 'super_admin/approve_request.html', context)

#------------background task expring request-------#   
@background(schedule=20)
def expire_request(pk):
    Request.objects.filter(id=pk).update(status="expired")
   

# running process tasks background
def process_tasks():
    process_tasks_cmd = "python manage.py process_tasks"
    process_tasks_ags = shlex.split(process_tasks_cmd)
    process_tasks_subprocess = subprocess.Popen(process_tasks_ags)

# request expired checker
def checker(request):
    req = Request.objects.all().first()
    if req:
        status = req.status

    else:
        status = 'none'

    
    return HttpResponse(status)

