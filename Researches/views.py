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
        return redirect('Researches:style', style_number=1)
    return render(request, 'age.html')

def style(request, style_number):
    if request.method == 'POST':
        style = request.POST.get(f'style{style_number}')
        request.session[f'style{style_number}'] = style
        next_style_number = style_number + 1
        if next_style_number <= 8:  # 스타일 8까지만 처리
            return redirect(f'Researches:style', style_number=next_style_number)
        else:
            return redirect('Researches:MBTI_EI')
    return render(request, f'style{style_number}.html')

def MBTI_EI(request):
    if request.method == 'POST':
        MBTI_EI = request.POST.get('MBTI_EI')
        request.session['MBTI_EI'] = MBTI_EI
        return redirect('Researches:MBTI_SN')
    return render(request, 'MBTI_EI.html')

def MBTI_SN(request):
    if request.method == 'POST':
        MBTI_SN = request.POST.get('MBTI_SN')
        request.session['MBTI_SN'] = MBTI_SN
        return redirect('Researches:MBTI_FT')
    return render(request, 'MBTI_SN.html')

def MBTI_FT(request):
    if request.method == 'POST':
        MBTI_FT = request.POST.get('MBTI_FT')
        request.session['MBTI_FT'] = MBTI_FT
        return redirect('Researches:MBTI_JP')
    return render(request, 'MBTI_FT.html')

def MBTI_JP(request):
    if request.method == 'POST':
        MBTI_JP = request.POST.get('MBTI_JP')
        request.session['MBTI_JP'] = MBTI_JP

        MBTI_EI = request.session['MBTI_EI']
        MBTI_SN = request.session['MBTI_SN']
        MBTI_FT = request.session['MBTI_FT']

        MBTI=MBTI_EI + MBTI_SN + MBTI_FT + MBTI_JP
        
        Question.objects.create(
            age=request.session['age'],
            gender=request.session['gender'],
            style1=request.session['style1'],
            style2=request.session['style2'],
            style3=request.session['style3'],
            style4=request.session['style4'],
            style5=request.session['style5'],
            style6=request.session['style6'],
            style7=request.session['style7'],
            style8=request.session['style8'],
            MBTI=MBTI,
        )
        return redirect('Researches:result')
    return render(request, 'MBTI_JP.html')

def result(request):
    return render(request, 'result.html')