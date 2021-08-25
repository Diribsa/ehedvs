from django.forms import ModelForm
from django.http import request
from .models import University
from accounts.models import User, RegistrarAdmin, RegistrarStaff
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.contrib.auth.models import Group

        
class AdminSignUpForm(UserCreationForm):
    university = forms.ModelChoiceField(queryset=University.objects.all(), empty_label="Please select unversity")
    password1 = forms.CharField(
            label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(
            label='Confirm Password(again)', widget=forms.PasswordInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['university','first_name','last_name','username', 'email' , 'password1', 'password2']
        help_texts = {
            'username': None,
            
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user. is_registrar_admin = True
        user.save()
        group = Group.objects.get(name='registrar_admin')
        user.groups.add(group)
        registrarAdmin = RegistrarAdmin.objects.create(user=user)
        registrarAdmin.university=self.cleaned_data.get('university')
        registrarAdmin.save()
        return user




class StaffSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self._loged_user=kwargs.pop('loged_user', None)
        super().__init__(*args, **kwargs)
    #university = forms.ModelChoiceField(queryset=University.objects.all(), empty_label="Please select your unversity")
    #university = forms.CharField(max_length=200)
    password1 = forms.CharField(
            label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(
            label='Confirm Password(again)', widget=forms.PasswordInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name','last_name','username', 'email' , 'password1', 'password2']
        help_texts = {
            'username': None,
            
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user. is_registrar_staff = True
        user.save()
        group = Group.objects.get(name='registrar_staff')
        user.groups.add(group)
        
       
        #univ = RegistrarAdmin.objects.get(user_id=userId)
        registrarStaff = RegistrarStaff.objects.create(user=user)
        #userId=request.user
        #registrarStaff.university=self.cleaned_data.get('university')
        registrarStaff.university_id=self._loged_user
        #userId=self._loged_user

        registrarStaff.save()
        #print(userId)
        return user
 

