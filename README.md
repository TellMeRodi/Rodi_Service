[작업순서]
1. 최신 데이터 가져오기 \
    git switch main \
    -> git pull origin main \
    -> git switch <내 브랜치> \
    -> git merge main 
     
2. 작업 진행 \
    git switch <내 브랜치> \
    -> 작업 \
    -> add / commit / push 
    
3. github에서 pull request -> merge


 \
[추천 시스템 api 연결방법]
1. 가상환경 활성화 \
source venv/Scripts/activate

2. requirements.txt 필요 모듈 설치 \
pip install -r requirements.txt

3. 새 터미널 에서 uvicorn api 서버실행

3-1. venv 활성화 \
source venv/Scripts/activate 

3-2. 경로 진입(Researches로) \
cd Researches

3-3. uvicorn 실행 \
python -m uvicorn main_api:app --reload --port 8001 


 \
[SQL연동]
1. RODI 폴더에 local_settings.py 파일 생성 -> 아래 내용 입력 \
-- 파일명이 다르면 github에 업로드시 아래 적은 비밀번호가 노출될 수 있으니 주의하세요! \
-- 이때 PASSWORD 란에는 본인의 root비밀번호를 입력하시면 됩니다. 
```
# 현재 데이터베이스의 값을 입력한다.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 사용할 데이터베이스 엔진
        'NAME': 'ResearchesDB', # 데이터베이스 이름 
        'USER': 'root', # 접속할 Database 계정 아이디 ex) root
        'PASSWORD': '__자신의 MySQL root비밀번호__',  # 접속할 Database 계정 비밀번호 ex) 1234
        'HOST': '127.0.0.1',   # host는 로컬 환경에서 동작한다면 ex) localhost
        'PORT': '3306', # 설치시 설정한 port 번호를 입력한다. ex) 3306
    }
}

# settings.py에 있던 시크릿 키를 아래 ''안에 입력한다.
SECRET_KEY = "django-insecure-yabkzw#8fzvend5_3_@46v4_%v)3swur7+^vi_aj(br!(ekl_#"


MySQL Workbench 실행 및 ResearchesDB 생성
-- 이때 사용자가 root 인지 확인
CREATE DATABASE IF NOT EXISTS ResearchesDB;
```

2. migtrate \
py manage.py migrate


3. MySQL에서 DB확인 \
SELECT * FROM researchesdb.researches_question;