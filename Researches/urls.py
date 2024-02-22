from django.urls import path
from . import views

app_name = 'Researches'

urlpatterns = [
    path('', views.home, name='home'),
    path('gender/', views.gender, name='gender'),
    path('age/', views.age, name='age'),    
    path('style1/', views.style1, name='style1'),
    path('style2/', views.style2, name='style2'),
    path('style3/', views.style3, name='style3'),
    path('style4/', views.style4, name='style4'),
    path('style5/', views.style5, name='style5'),
    path('style6/', views.style6, name='style6'),
]