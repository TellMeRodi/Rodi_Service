from django.shortcuts import render, redirect
from .models import Question
import requests
from . import matrics_describe

# Create your views here.
def home(request):
    return render(request, 'home.html')

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
        return redirect('Researches:style1')
    return render(request, 'style3.html')

def style1(request):
    if request.method == 'POST':
        style1 = request.POST.get('style1')
        request.session['style1'] = style1
        return redirect('Researches:style4')
    return render(request, 'style1.html')

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
        return redirect('Researches:style8')
    return render(request, 'style5.html')

def style8(request):
    if request.method == 'POST':
        style8 = request.POST.get('style8')
        request.session['style8'] = style8
        return redirect('Researches:style6')
    return render(request, 'style8.html')

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
        return redirect('Researches:MBTI_EI')
    return render(request, 'style7.html')

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
        return redirect('Researches:gender')
    return render(request, 'MBTI_JP.html')

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

        MBTI_EI = request.session['MBTI_EI']
        MBTI_SN = request.session['MBTI_SN']
        MBTI_FT = request.session['MBTI_FT']
        MBTI_JP = request.session['MBTI_JP']

        MBTI=MBTI_EI + MBTI_SN + MBTI_FT + MBTI_JP
        
        Question.objects.create(
            age=age,
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
        return redirect('Researches:surveyend')
    return render(request, 'age.html')

def definite_data(session):
    MBTI_EI = session.get('MBTI_EI')
    MBTI_SN = session.get('MBTI_SN')
    MBTI_FT = session.get('MBTI_FT')
    MBTI_JP = session.get('MBTI_JP')

    MBTI = MBTI_EI + MBTI_SN + MBTI_FT + MBTI_JP
    
    data = {
        'age': session.get('age'),
        'gender': session.get('gender'),
        'style1': session.get('style1'),
        'style2': session.get('style2'),
        'style3': session.get('style3'),
        'style4': session.get('style4'),
        'style5': session.get('style5'),
        'style6': session.get('style6'),
        'style7': session.get('style7'),
        'style8': session.get('style8'),
        'MBTI': MBTI,
    }
    return data

def surveyend(request):
    if request.method == 'POST':
        return redirect('Researches:recommendations')
    return render(request, 'surveyend.html')

def get_recommendations(request):
    data = definite_data(request.session)
    # FastAPI 엔드포인트 URL
    fastapi_url = "http://localhost:8001/home/recommendations/"
    
    # 장고 뷰로 받은 데이터를 FastAPI 엔드포인트로 전달
    response = requests.post(fastapi_url, json=data)  # 수정된 부분
    
    # FastAPI의 응답 처리
    if response.status_code == 200:
        recommended_cities = response.json().get('recommended_cities', [])
        traveler_type = response.json().get('traveler_type', [])
        traveler_type_cities = response.json().get('traveler_type_cities', [])
        matrics_des = matrics_describe.matrics_des
        context = {'recommended_cities': recommended_cities,
                   'traveler_type': traveler_type, 
                   'traveler_type_cities': traveler_type_cities,
                   'type_photo': matrics_des[traveler_type]['photo'],
                   'type_keyword': matrics_des[traveler_type]['keyword'],
                   'type_descr': matrics_des[traveler_type]['describe'],}
    else:
        context = {'error': 'API 호출에 실패했습니다.'}

    return render(request, 'result.html', context)