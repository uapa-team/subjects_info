from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.api_logout, name='Destroy token on REST API'),

    path('get_schedule', views.get_schedule, name='get_schedule'),
    path('create_schedule', views.create_schedule, name='create_schedule'),
    path('submit_form', views.submit_form, name='submit_form'),
    path('subjects', views.get_subjects, name='subjects'),
    path('get_code', views.get_code, name='get_code')
]
