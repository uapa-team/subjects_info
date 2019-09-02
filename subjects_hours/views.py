from django.shortcuts import render
from .models import PersonSubject
from django.http import HttpResponse
from .sia_script.EstudianteSia import EstudianteSia
from .communication import get_dni, get_subject_name
from django_auth_ldap.backend import LDAPBackend


def index(request):
    return render(request, 'subjects_hours/login.html')


def survey_view(request, user=''):
    if request.method == 'POST':
        dni = get_dni(user)
        student = EstudianteSia(dni)
        context = {
            'dni': dni,
            'schedule': student.schedule,
            'names': [get_subject_name(code) for code in student.schedule[0]]
        }
        return render(request, 'subjects_hours/form.html', context)
    else:
        return render(request, 'subjects_hours/login.html')
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
            return survey_view(request, username)
    else:
        return render(request, 'subjects_hours/login.html')
