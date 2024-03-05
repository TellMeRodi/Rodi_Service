# 현재 데이터베이스의 값을 입력한다.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 사용할 데이터베이스 엔진
        'NAME': 'ResearchesDB', # 데이터베이스 이름 
        'USER': 'Rodi', # 접속할 Database 계정 아이디 ex) root
        'PASSWORD': '!@Rodi1234',  # 접속할 Database 계정 비밀번호 ex) 1234
        'HOST': '13.208.95.65',   # host는 로컬 환경에서 동작한다면 ex) localhost
        'PORT': '8913', # 설치시 설정한 port 번호를 입력한다. ex) 3306
    }
}

# settings.py에 있던 시크릿 키를 아래 ''안에 입력한다.
SECRET_KEY = "django-insecure-yabkzw#8fzvend5_3_@46v4_%v)3swur7+^vi_aj(br!(ekl_#"