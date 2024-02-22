from django.shortcuts import render, redirect
from .models import Question

# Create your views here.
def home(request):
    return render(request, 'home.html')

def gender(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        request.session['gender'] = gender
        return redirect('Researches:age')
    return render(request, 'gender.html')