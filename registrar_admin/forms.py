from django import forms
from super_admin.models import University
from django.forms import ModelForm
from .models import Faculty, Program
from django.db import transaction
class FacultyForms(ModelForm):
    def __init__(self, *args, **kwargs):
        self._loged_user=kwargs.pop('loged_user', None)
        super().__init__(*args, **kwargs)
       
    #university = forms.CharField(max_length=300)
    

    class Meta:
        model=Faculty
        fields=['name', 'total_programs']
        labels = {
        'name':'Name of faculty',
        
        }
    def save(self):
        school = super().save(commit=False)
        fclt = Faculty.objects.create(university=self._loged_user ,
         name=school, total_programs=school.total_programs)


    

class ProgramForms(ModelForm):
    class Meta:
        model=Program
        fields='__all__'
        labels = {
        'name':'Name of program',
        
        }
        
    def __init__(self, logged_univ, *args, **kwargs):
        super(ProgramForms, self).__init__(*args,**kwargs)
        self.fields['faculty'].queryset=Faculty.objects.filter(university=logged_univ)

