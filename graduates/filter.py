from django.db.models import fields
import django_filters
from django_filters import CharFilter
from .models import *
from django import forms

class AcademicFilter(django_filters.FilterSet):
    class Meta:
        model = AcademicHistory
        fields = '__all__'
        exclude = [ 'student','uploaded_by','uploaded_date']


class StudentFilter(django_filters.FilterSet):
    #name = CharFilter(field_name='first_name', lookup_expr='icontains')
    class Meta:
        model= Student
        fields = ['id']
        
        