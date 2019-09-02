from django.shortcuts import render
from .models import PersonSubject
from django.http import HttpResponse
# from .sia_script.EstudianteSia import EstudianteSia
from django_auth_ldap.backend import LDAPBackend


def index(request):
    return render(request, 'subjects_hours/login.html')


def survey_view(request):
    return HttpResponse("prueba")
#     if request.method == 'POST':
#         dni = request.POST['dni']
#         student = EstudianteSia(dni)
#         context = {
#             'dni': dni,
#             'carrers': {}
#         }

#         for ha in student.dp.ha:
#             context[ha] = {
#                 'name': student.dp.ha[ha]['programa'].split('|')[1],
#                 'schedule': []
#             }

#         return render(request, 'subjects_hours/form.html', context)
#     else:
#         return render(request, 'subjects_hours/login.html')


def submit_form(request):
    if request.method == 'POST':
        hours = request.POST.getlist('hours')
        subject = PersonSubject(dni_person="123456798", period="2019-01", dedication_hours=hours[0],
                                autonomous_hours=hours[1], accompaniment_hours=hours[2], cod_subject_id="1234567")
        subject.save()
        return HttpResponse('')
    else:
        return render(request, 'form.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pass')
        auth = LDAPBackend()
        user = auth.authenticate(
            request, username=username,  password=password)
        if user is None:
            return HttpResponse('Not Authenticated! :c')
        else:
            return HttpResponse('Authenticated!')
    else:
        return render(request, 'subjects_hours/login.html')
