from django.shortcuts import render
from .models import PersonSubject, Subject
from django.http import HttpResponse
from .sia_script.EstudianteSia import EstudianteSia
from .communication import get_dni, get_subject_name
from django_auth_ldap.backend import LDAPBackend
from datetime import date

def index(request):
    return render(request, 'subjects_hours/login.html')


def survey_view(request, user=''):
    if request.method == 'POST':
        dni = get_dni(user)
        student = EstudianteSia(dni)
        context = {
            'dni': dni,
            'schedule': [
                [code[1:],
                get_subject_name(code.split(' - ')[0][1:])] 
                for code in student.schedule[0]
                ]
        }
        return render(request, 'subjects_hours/form.html', context)
    else:
        return render(request, 'subjects_hours/login.html')
        
def submit_form(request):
    if request.method == 'POST':
        codes = [code.split(' - ')[0] for code in request.POST.getlist('code')]
        names = request.POST.getlist('name')
        
        for i in range(len(codes)):
            try:
                Subject.objects.get(pk=codes[i])
            except Exception:
                Subject(cod_subject=codes[i], name=names[i]).save()
        
        hours = request.POST.getlist('hours')

        for i in range(0, len(hours), 3):
            subject = PersonSubject(
                dni_person=request.POST.get('dni'),
                period="2019-2S",
                dedication_hours=hours[i+0],
                autonomous_hours=hours[i+1],
                accompaniment_hours=hours[i+2],
                cod_subject_id=codes[int(i/3)]
                date = date.today()
                )
            subject.save()
        return HttpResponse(Subject.objects)
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
