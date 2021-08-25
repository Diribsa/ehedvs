from django.forms import ModelForm, fields
from django import forms
from .models import AcademicHistory, Profile, Student
from accounts.models import RegistrarStaff
from registrar_admin.models import Faculty, Program

class AcademicHistoryForm(ModelForm):
    class Meta:
        model=AcademicHistory
        fields='__all__'

class StudentForm(ModelForm):
        class Meta:
             model=Student
             fields=['id','school', 'department']
        def __init__(self, user, *args,  **kwargs):
            super(StudentForm, self).__init__(*args, **kwargs)
            logged_admin_univ=RegistrarStaff.objects.get(user=user).university
            self.fields['school'].queryset=Faculty.objects.filter( university=logged_admin_univ)
            self.fields['department'].queryset=Program.objects.filter(faculty__university = logged_admin_univ)
            self.fields['id'].widget.attrs['readonly']=True
            
                 


def update_dept(user):

    class StudentForm(ModelForm):
        class Meta:
             model=Student
             fields=['id','school', 'department']

        def __init__(self, *args,  **kwargs):
             super(StudentForm, self).__init__(*args, **kwargs)
             if user:
                 logged_admin_univ=RegistrarStaff.objects.get(user=user).university
                 self.fields['school'].queryset=Faculty.objects.filter( university=logged_admin_univ)
                 self.fields['department'].queryset=Program.objects.filter(faculty__university = logged_admin_univ)
                 self.fields['id'].widget.attrs['readonly']=True
    return StudentForm
    



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class DateInput(forms.DateInput):
    input_type= 'date'
    

class ExapleForm(forms.Form):
    Select_date = forms.DateField( widget=DateInput)
    