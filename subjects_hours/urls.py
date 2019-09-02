from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('survey_view', views.survey_view, name='survey_view'),
    path('submit_form', views.submit_form, name='submit_form'),
    path('login', views.login, name='login'),
]
