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

def style2(request):
    if request.method == 'POST':
        style2 = request.POST.get('style2')
        request.session['style2'] = style2
        return redirect('Researches:style3')
    return render(request, 'style2.html')

def style3(request):
    if request.method == 'POST':
        style3 = request.POST.get('style3')
        request.session['style3'] = style3
        return redirect('Researches:style4')
    return render(request, 'style3.html')

def style4(request):
    if request.method == 'POST':
        style4 = request.POST.get('style4')
        request.session['style4'] = style4
        return redirect('Researches:style5')
    return render(request, 'style4.html')

def style5(request):
    if request.method == 'POST':
        style5 = request.POST.get('style5')
        request.session['style5'] = style5
        return redirect('Researches:style6')
    return render(request, 'style5.html')

def style6(request):
    if request.method == 'POST':
        style6 = request.POST.get('style6')
        request.session['style6'] = style6
        return redirect('Researches:style7')
    return render(request, 'style6.html')

def style7(request):
    if request.method == 'POST':
        style7 = request.POST.get('style7')
        request.session['style7'] = style7
        return redirect('Researches:style8')
    return render(request, 'style7.html')

def style8(request):
    if request.method == 'POST':
        style8 = request.POST.get('style8')
        request.session['style8'] = style8
        return redirect('Researches:MBTI_EI')
    return render(request, 'style8.html')

def MBTI_EI(request):
    if request.method == 'POST':
        MBTI_EI = request.POST.get('MBTI_EI')
        request.session['MBTI_EI'] = MBTI_EI
        return redirect('Researches:MBTI_SN')
    return render(request, 'MBTI_EI.html')