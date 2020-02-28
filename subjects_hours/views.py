# pylint: disable=wildcard-import,unused-wildcard-import
import json
from .models import Subject, PersonSchedule, RegisterHour
from django.http import HttpResponse, JsonResponse
from .communication import get_dni, get_name, get_subject_name
from django_auth_ldap.backend import LDAPBackend
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import *
from django.contrib.auth import logout

CURRENT_PERIOD = '2020-1S'


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    auth = LDAPBackend()
    user = auth.authenticate(
        request, username=username, password=password)
    if not user:
        return JsonResponse({'error': 'Error en LDAP, contraseña o usuario no válido.'},
                            status=HTTP_404_NOT_FOUND)
    # pylint: disable=no-member
    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({'token': token.key, 'name': get_name(username)},
                        status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def api_logout(request):
    request.auth.delete()
    logout(request)
    return JsonResponse({'successful': 'Logout Success'}, status=HTTP_200_OK)


@api_view(["GET"])
def get_schedule(request):
    user = request.user.username
    dni = get_dni(user)
    # pylint: disable=no-member
    schedule = PersonSchedule.objects.filter(
        dni_person=dni, period=CURRENT_PERIOD)

    if schedule.exists():
        codes = [sub.cod_subject.cod_subject for sub in schedule]
    else:
        codes = []
    count = 0
    subjects = []
    for code in codes:
        exist = Subject.objects.get(pk=code)
        name = exist.name if exist else 'N/A'
        subjects.append({
            'key': count,
            'subject_cod': code,
            'subject_name': name,
            'dedication_hours': '',
            'autonomous_hours': '',
            'accompaniment': ''
        })
        count += 1
    return JsonResponse({'username': user, 'subjects': subjects}, status=HTTP_200_OK)


@api_view(["POST"])
def create_schedule(request):
    # pylint: disable=no-member
    subjects = json.loads(request.body)['subjects']
    user = request.user.username
    dni = get_dni(user)
    errors = []
    for subject in subjects:
        try:
            ref = Subject.objects.get(pk=subject['subject_cod'])
            if len(PersonSchedule.objects.filter(
                dni_person=dni, cod_subject=ref,
                group=subject['group'], period=CURRENT_PERIOD
            )) == 0:
                PersonSchedule(
                    dni_person=dni, cod_subject=ref,
                    group=subject['group'], period=CURRENT_PERIOD
                ).save()
        except:
            errors.append(subject['code'])
    return JsonResponse({'errors': errors}, status=HTTP_200_OK)


@api_view(["POST"])
def submit_form(request):
    data = json.loads(request.body)
    dni = get_dni(request.user.username)

    for subject in data['subjects']:
        code = subject['subject_cod']
        RegisterHour(
            # pylint: disable=no-member
            schedule=PersonSchedule.objects.filter(
                dni_person=dni, cod_subject=code, period=CURRENT_PERIOD).last(),
            dedication_hours=subject['dedication_hours'],
            autonomous_hours=subject['autonomous_hours'],
            accompaniment_hours=subject['accompaniment']
        ).save()
    return JsonResponse({'registered': 'Ok'}, status=HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_subjects(_):
    # pylint: disable=no-member
    subjects = Subject.objects.all()
    response = []
    for subject in subjects:
        response.append({
            'subject_cod': subject.cod_subject,
            'subject_name': subject.name
        })
    return JsonResponse({'subjects': response}, status=200)
