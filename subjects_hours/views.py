import json
from django.shortcuts import render
from .models import PersonSubject, Subject
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
        print(user)
        dni = get_dni(user)
        student = EstudianteSia(dni)

        subjects = []
        count = 0
        for schedule in student.schedule:
            for code in schedule:
                subjects.append({
                    'key': count,
                    'subject_cod': code[1:],
                    'subject_name': get_subject_name(code.split(' - ')[0][1:]),
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
            code = subject['subject_cod'].split(' - ')[0]
            try:
                Subject.objects.get(pk=subject['subject_cod'])
            except Exception:
                Subject(cod_subject=code, name=subject['subject_name']).save()

            PersonSubject(
                dni_person=dni,
                period="2019-2S",  # TODO: Calcular periodo
                dedication_hours=subject['dedication_hours'],
                autonomous_hours=subject['autonomous_hours'],
                accompaniment_hours=subject['accompaniment'],
                cod_subject_id=code
            ).save()
        return HttpResponse(True, status=200)
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
