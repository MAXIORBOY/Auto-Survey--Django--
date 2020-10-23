from django.urls import path, include
from django.contrib import admin
from .models import Survey
from . import views

urlpatterns = [
path("", views.home_page, name='home_page'),
path("<int:page>/", views.home_page, name='home_page'),
path('archives/', views.home_page, {'mode': 'archives'}, name='home_page'),
path('archives/<int:page>/', views.home_page, {'mode': 'archives'}, name='home_page'),
path('current/', views.home_page, {'mode': 'current'}, name='home_page'),
path('current/<int:page>/', views.home_page, {'mode': 'current'}, name='home_page'),
path('search/', views.home_page, name='home_page'),
path('search/page=<int:page>/search=<str:search>', views.home_page, name='searching')
]
try:
    survey_names = list(Survey.objects.all())
    urlpatterns.extend([path(str(survey_names[i]).replace(' ', '_') + '/', views.survey, name=str(survey_names[i]).replace(' ', '_')) for i in range(len(survey_names))])
except:
    pass
