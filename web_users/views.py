from registrar_admin.models import Faculty, Program
from django.http.response import HttpResponse
from django.shortcuts import render
from graduates.models import AcademicHistory, Student

def web_user(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:

            try:
                graduate = Student.objects.get(id=q)
                gra=None
                degree_type=None
                print(graduate.level_of_completion)
                print(graduate.department)
                if graduate:
                    if graduate.level_of_completion==100.0:
                        year_required = Program.objects.get(name=graduate.department).year_required
                        degree_type = Program.objects.get(name=graduate.department).degree_type
                        print(degree_type)
                        print(year_required)
                        try:
                            gra = AcademicHistory.objects.get(student=q, batch=year_required, semester=2)
                        
                        except AcademicHistory.DoesNotExist:
                            return render(request, 'web_users/index.html',
                              {'search': q,
                               'error_message': 'This Student seems  has not completed the program yet'
                               })

                        
                    return render(request, 'web_users/index.html', {'student': graduate, 'gra':gra, 'degree_type':degree_type})
                

            except Student.DoesNotExist:
                return render(request, 'web_users/index.html',
                              {'search': q,
                               'error_message': 'Sorry No result found with a keyword you entered'
                               })

        else:
            return render(request, 'web_users/index.html')


    return render(request, 'web_users/index.html')


def certificate(request):

    context = {'q':'qq'}
    return render(request, 'web_users/index.html', context)

