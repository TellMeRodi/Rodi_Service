from django.urls import path
from . import views

app_name = 'Researches'

urlpatterns = [
    path('', views.home, name='home'),
    path('gender/', views.gender, name='gender'),
    path('age/', views.age, name='age'),    
]