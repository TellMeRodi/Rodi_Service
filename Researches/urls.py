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
    path('style7/', views.style7, name='style7'),
    path('style8/', views.style8, name='style8'),
    path('MBTI_EI/', views.MBTI_EI, name='MBTI_EI'),
    path('MBTI_SN/', views.MBTI_SN, name='MBTI_SN'),
    path('MBTI_FT/', views.MBTI_FT, name='MBTI_FT'),
]