from django.http.response import HttpResponse
from super_admin.models import University, ActivityLog
from django.shortcuts import redirect, render
from .forms import FacultyForms, ProgramForms
from. models import Faculty,Program, Request
from accounts.models import RegistrarStaff, RegistrarAdmin,User
from accounts.forms import StaffSignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from accounts.decorators import registrar_admin
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from graduates.models import Student, AcademicHistory



@login_required(login_url='accounts:login')
@registrar_admin
def dashboard(request):
    logged_user = request.user
    logged_admin_univ=RegistrarAdmin.objects.get(user=logged_user).university
    print(logged_admin_univ)
    faculties = Faculty.objects.filter( university=logged_admin_univ).order_by('-id')[0:5]
    programs = Program.objects.filter(faculty__university = logged_admin_univ).order_by('-id')[0:5]
        
    return render(request, 'registrar_admin/dashboard.html',{'faculties':faculties, 'programs':programs})

@login_required(login_url='accounts:login')
@registrar_admin
def faculty(request):
    logged_user = request.user
    logged_admin_univ=RegistrarAdmin.objects.get(user=logged_user).university
    faculties = Faculty.objects.filter(university = logged_admin_univ).order_by('-id')[0:5]
    loged=request.user.id
    univ = RegistrarAdmin.objects.get(pk=loged).university
    form = FacultyForms()
    if request.method == 'POST':
        try:
            form = FacultyForms(request.POST, loged_user=univ)
            if form.is_valid():
                form.save()
                return redirect('/registrar_admin/faculty')
         

        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                #return redirect('/accounts/exist/')
                messages.warning(request,'This Faculty already exist')
                

    return render(request, 'registrar_admin/faculty.html', {'form':form, 'faculties':faculties})

@login_required(login_url='accounts:login')
@registrar_admin
def program(request):
   programs = Program.objects.all().order_by('-id')[0:5]
   logged_univ = RegistrarAdmin.objects.get(user=request.user).university
   program = ProgramForms(logged_univ)
   try:
       if request.method == 'POST':
           program = ProgramForms(logged_univ, request.POST)
           if program.is_valid:
               program.save()
               return redirect('/registrar_admin/program')

   
   except ValueError:
           print(program.errors)
   
   
   return render(request, 'registrar_admin/program.html', { 'program':program, 'programs':programs})


def delete_faculty(request, id):
    school = Faculty.objects.get(id=id)
    school.delete()
    return redirect('/registrar_admin')

def delete_program(request, id):
    school = Program.objects.get(id=id)
    school.delete()
    return redirect('/registrar_admin')


def update_faculty(request, id):
    faculty = Faculty.objects.get(id=id)
    form = FacultyForms(instance=faculty)
    loged=request.user.id
    univ = RegistrarAdmin.objects.get(pk=loged).university
    if request.method == 'POST':
        try:
            form = FacultyForms( request.POST, instance=faculty, loged_user=univ,)
            if form.is_valid():
                form.save()
                return redirect('/registrar_admin/')
         

        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                #return redirect('/accounts/exist/')
                messages.warning(request,'This Faculty already exist')
    context = {'form': form}
    return render(request, 'registrar_admin/faculty.html', context)



#update program
def update_program(request, id ):
    pro = Program.objects.get(id=id)
    logged_univ = RegistrarAdmin.objects.get(user=request.user).university
    program = ProgramForms(logged_univ,instance=pro)
    try:
       if request.method == 'POST':
           program = ProgramForms(logged_univ, request.POST, instance=pro)
           if program.is_valid:
               program.save()
               return redirect('/registrar_admin/')

    except ValueError:
           print(program.errors)

    context = {'program':program}
    return render(request, 'registrar_admin/program.html', context)

#register registrar_staff
@login_required(login_url='accounts:login')
@registrar_admin
def createAccount(request):
    form = StaffSignUpForm()
    loged=request.user.id
    univ = RegistrarAdmin.objects.get(pk=loged).university_id
    #form.fields['university'].initial=univ


    if request.method=='POST':
        form = StaffSignUpForm(request.POST, loged_user=univ)
        if form.is_valid():
            form.save()
            return redirect('/registrar_admin/user_profile')

        else:
            messages.warning(request,'the two password doesnot match')
    context = {'form': form}
    return render(request, 'registrar_admin/account.html', context)

# delete User
def deleteRegStaff(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/registrar_admin/")

#user profile
@login_required(login_url='accounts:login')
@registrar_admin
def useProfile(request):
    logged_user = request.user
    univ = RegistrarAdmin.objects.get(user=logged_user).university
    lists = RegistrarStaff.objects.filter(university=univ).order_by('-user_id')[:6]

    context = {'lists':lists}
    return render(request, 'registrar_admin/user_profile.html', context)




# activity logs
def activity_logs(request):
    logged_admin = request.user
    logged_university = RegistrarAdmin.objects.get(user=logged_admin).university
    top_three_staffs = RegistrarStaff.objects.filter(university=logged_university)[:3]
    activities = ActivityLog.objects.filter(institution=logged_university).exclude(user__is_registrar_admin=True)
    academic_upload = ActivityLog.objects.filter(operation="academic_upload" , institution=logged_university).count()
    acadmic_status_deletion = ActivityLog.objects.filter(operation="acadmic_status_deletion" , institution=logged_university).count()
    student_registry = ActivityLog.objects.filter(operation="student_registry", institution=logged_university).count()
    certificate_generation = ActivityLog.objects.filter(operation="student_deletion", institution=logged_university).count()
    student_deletion = ActivityLog.objects.filter(operation="certificate_generation", institution=logged_university).count()
    context = {

       'activities':activities,
       'academic_upload':academic_upload,
       'acadmic_status_deletion':acadmic_status_deletion,
       'student_registry':student_registry,
       'certificate_generation': certificate_generation,
       'student_deletion':student_deletion,
    }
    return render(request, 'registrar_admin/activiy_logs.html', context)

#certificate archive

def certificate_archive(request):
     certificates = Student.objects.filter(level_of_completion=100.0)

    
     context = {
        'certificates': certificates,

    }
    
     return render(request, 'registrar_admin/certificate_archive.html', context)

# graduate detail
def status_detail(request, id):
    name = Student.objects.get(id=id)
    dept = name.department
    required_year= Program.objects.get(name=dept).year_required
    print(required_year)
    graduate = AcademicHistory.objects.get(student=id, batch=required_year, semester=2)
    student = AcademicHistory.objects.filter(student=id)
    context = {'students': student, 'name': name, 'graduate':graduate}
    return render(request, 'registrar_admin/status_detail.html', context)

# sending request to super_admin
def send_request(request):
    logged_user = request.user
    registrar_admin=RegistrarAdmin.objects.get(user=logged_user)
    requests = Request.objects.filter(sender=registrar_admin)[0:4]
    messages = Request.objects.filter(sender=registrar_admin)[0:1]
    if request.method =='POST':
        subject = request.POST.get('subject')
        super_admin = get_user_model().objects.get(is_superuser=True)
        logged_user = request.user
        registrar_admin=RegistrarAdmin.objects.get(user=logged_user)
        Request.objects.create(sender=registrar_admin, reciever=super_admin, request=subject)
        #process_tasks()
        
        
    context ={
        'requests':requests,
        'messages':messages
    }
    return render(request, 'registrar_admin/request.html', context)


def delete_request(request, id):
    rqst = Request.objects.get(id=id)
    rqst.delete()
    return redirect('/registrar_admin/send_request/')

