import json
from .models import Subject, PersonSchedule, RegisterHour
from django.http import HttpResponse, JsonResponse
from .communication import get_dni, get_name, get_subject_name
from django_auth_ldap.backend import LDAPBackend
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def survey_view(request):
    user = json.loads(request.body)['username']
    dni = get_dni(user)
    schedule = PersonSchedule.objects.filter(
        dni_person=dni, period='2019-2S')

    if schedule.exists():
        codes = [sub.cod_subject.cod_subject for sub in schedule]
    else:
        codes = []
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


def create_schedule(dni, code, group):
    if not Subject.objects.filter(cod_subject=code).exists():
        Subject(cod_subject=code,
                name=get_subject_name(code)).save()
    PersonSchedule(
        dni_person=dni,
        cod_subject=Subject.objects.get(pk=code),
        group=group, period='2019-2S'
    ).save()


@csrf_exempt
def submit_form(request):
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


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    auth = LDAPBackend()
    user = auth.authenticate(
        request, username=username, password=password)
    if user is None:
        return HttpResponse(False, status=404)
    return HttpResponse(get_name(username), status=200)
