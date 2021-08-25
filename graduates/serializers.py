from import_export import fields
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import AcademicHistory, Student, Profile

class CertificateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source = 'student.full_name')
    institution  = serializers.CharField(source = 'student.institution')
    logo  = serializers.CharField(source = 'student.institution.logo')
    dept = serializers.CharField(source = 'student.department')
    school = serializers.CharField(source = 'student.school')
    level_of_completion=serializers.CharField(source = 'student.level_of_completion')
    date = serializers.CharField(source='uploaded_date')
    class Meta:
        model = AcademicHistory
        fields = ['student', 'full_name', 'institution', 'logo', 'school', 'dept','GPA','CGPA' , 'date' , 'level_of_completion']



class StudentSerializer(ModelSerializer):
    institution = serializers.ReadOnlyField(source ='institution.name')
    class Meta:
        model=Student
        fields = ('id','first_name','middle_name','last_name','institution')
        
    
class ProfileSerializer( serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields =['student', 'image',]
        


  