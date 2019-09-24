import json
from django.shortcuts import render
from .models import Subject, PersonSchedule, RegisterHour
from django.http import HttpResponse, JsonResponse
from .sia_script.EstudianteSia import EstudianteSia
from .communication import get_dni, get_name, get_subject_name
from django_auth_ldap.backend import LDAPBackend
from datetime import date
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def survey_view(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        dni = get_dni(user)
        schedule = PersonSchedule.objects.filter(
            dni_person=dni, period='2019-2S')

        if schedule.exists():
            codes = [sub.cod_subject.cod_subject for sub in schedule]
        else:
            student = EstudianteSia(dni)
            codes = []
            for schedules in student.schedule:
                for code in schedules:
                    info = code.split(' - ')
                    code = info[0][1:]
                    if not Subject.objects.filter(cod_subject=code).exists():
                        Subject(cod_subject=code,
                                name=get_subject_name(code)).save()
                    PersonSchedule(
                        dni_person=dni,
                        cod_subject=Subject.objects.get(pk=code),
                        group=info[1], period='2019-2S'
                    ).save()
                    codes.append(code)
        count = 0
        subjects = []
        for code in codes:
            subjects.append({
                'key': count,
                'subject_cod': code,
                'subject_name': get_subject_name(code),
                'dedication_hours': '',
                'autonomous_hours': '',
                'accompaniment': ''
            })
            count += 1
        response = {'username': user, 'subjects': subjects}
        return JsonResponse(response, status=200)
    else:
        return render(request, 'subjects_hours/login.html')


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dni = get_dni(data['username'])

        for subject in data['subjects']:
            code = subject['subject_cod']
            RegisterHour(
                schedule=PersonSchedule.objects.filter(
                    dni_person=dni, cod_subject=code, period='2019-2S')[0],
                dedication_hours=subject['dedication_hours'],
                autonomous_hours=subject['autonomous_hours'],
                accompaniment_hours=subject['accompaniment']
            ).save()
        return HttpResponse(True, status=201)
    else:
        return HttpResponse(False, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth = LDAPBackend()
        user = auth.authenticate(
            request, username=username,  password=password)
        if user is None:
            return HttpResponse(False, status=404)
        else:
            return HttpResponse(get_name(username), status=200)
    else:
        return render(request, 'subjects_hours/login.html')
