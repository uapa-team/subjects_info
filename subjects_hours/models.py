from django.utils import timezone
from django.db import models


class Subject(models.Model):
    cod_subject = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)


class PersonSchedule(models.Model):
    dni_person = models.CharField(max_length=20)
    cod_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.CharField(max_length=3, default='1')
    period = models.CharField(max_length=10)


class RegisterHour(models.Model):
    schedule = models.ForeignKey(PersonSchedule, on_delete=models.CASCADE)
    dedication_hours = models.IntegerField()
    autonomous_hours = models.IntegerField()
    accompaniment_hours = models.IntegerField()
    date = models.DateField(default=timezone.now)
