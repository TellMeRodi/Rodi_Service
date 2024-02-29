from django.urls import path
from . import views
from .views import research

app_name = 'Researches'

urlpatterns = [
    path('', views.home, name='home'),
    path('gender/', views.gender, name='gender'),
    path('age/', views.age, name='age'),    
    path('style<int:style_number>/', views.style, name='style'),
    path('MBTI_EI/', views.MBTI_EI, name='MBTI_EI'),
    path('MBTI_SN/', views.MBTI_SN, name='MBTI_SN'),
    path('MBTI_FT/', views.MBTI_FT, name='MBTI_FT'),
    path('MBTI_JP/', views.MBTI_JP, name='MBTI_JP'),
    path('recommendations/', views.get_recommendations, name='recommendations'),
]