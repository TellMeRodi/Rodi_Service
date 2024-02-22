from django.urls import path
from . import views
from .views import research



app_name = 'Researches'

urlpatterns = [
    path('', views.home, name='home'),
    path('research/', views.research, name='research'),
    
]