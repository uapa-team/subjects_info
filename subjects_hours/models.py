from django.utils import timezone
from django.db import models
from datetime import date


class Subject(models.Model):
    cod_subject = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    typology = models.CharField(max_length=1, default="")


class PersonSubject(models.Model):
    dni_person = models.CharField(max_length=20)
    cod_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    period = models.CharField(max_length=10)
    dedication_hours = models.IntegerField()
    autonomous_hours = models.IntegerField()
    accompaniment_hours = models.IntegerField()
    date = models.DateField(default=timezone.now)
