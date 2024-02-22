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

def age(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        request.session['age'] = age
        return redirect('Researches:style1')
    return render(request, 'age.html')

def style1(request):
    if request.method == 'POST':
        style1 = request.POST.get('style1')
        request.session['style1'] = style1
        return redirect('Researches:style2')
    return render(request, 'style1.html')