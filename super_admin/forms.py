from django.forms import ModelForm
from .models import University

class UniversityForm(ModelForm):
    class Meta:
        model=University
        fields='__all__'
        labels = {
        'pob':'Post Box Office',
        'phone_no1': 'Phone number 1',
        'phone_no2': 'Phone number 2',
        'fax_no':'Fax number',
        'website':'Website address'
        }