# 5. settings와 requirements 파일

## 5.1 버전 관리되지 않는 로컬 세팅은 피하도록 한다.

- 

## 5.2 여러 개의 settings 파일 이용하기

- 

## 5.3 코드에서 설정 분리하기

- 


## 5.4 환경 변수를 이용할 수 없을 때

- 비밀 파일 패턴(secrets file pattern) 방법 이용
    1. Json, Config, YAML, XML 중 한 가지 포맷으로 비밀 파일 생성
    2. 비밀 파일을 관리하기 위한 비밀 파일 로더를 추가
    3. 비밀 파일의 이름을 .gitignore에 추가

### 5.4.1 JSON 파일 이용하기

- secrets.json
~~~
{
    "SECRET_KEY": "w9y6_!%2x$rwe@4oufp%zyg@f3f1evq-36^my",
}
~~~

- settings.py 
~~~
import json

with open("secrets.json") as f:
    secrets = json.loads(f.read())
SECRET_KEY = secrets['SECRET_KEY']
~~~

### 5.4.2 Config, YAML, XML 파일 이용하기

- 다른 형태의 포맷을 이용할 때는 26.9 참고

## 5.5 여러 개의 requirements 파일 이용하기

- 각 세팅 파일에 해당하는 requirements 파일을 이용
- 각 서버에 필요한 컴포넌트만 설치
~~~
requirements/
    base.txt
    local.txt
    staging.txt
    production.txt
~~~

- base.txt 파일에는 모든 환경에서 필요한 패키지 작성
- local.txt 파일에는 개발 환경에 필요한 패키지 작성 
~~~
-r base.txt
coverage==3.7.1
django-debug-toolbar==1.3.0
~~~

### 5.5.1 여러 개의 requirements 파일로부터 설치하기

~~~
$ pip install -r requirements/local.txt
$ pip install -r requirements/production.txt
~~~

### 5.5.2 여러 개의 requirements 파일을 PaaS환경에서 이용하기

- 30장 참고

## 5.6 settings에서 파일 경로 처리하기

- settings 파일에 하드 코딩된 파일 경로는 작성 금지
- Unipath 패키지 이용
~~~
from unipath import Path

BASE_DIR = Path(__file__).ancestor(3)
MEDIA_ROOT = BASE_DIR.child('media')
STATIC_ROOT = BASE_DIR.child('static')
STATICFILES_DIRS = (
    BASE_DIR.child('assets'),
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        DIRS = (BASE_DIR.child('templates'),),
    },
]
~~~
- os.path 라이브러리 이용
~~~
from os.path import join, abspath, dirname

here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)
BASE_DIR = here("..", "..")
root = lambda *dirs: join(abspath(BASE_DIR), *dirs)

MEDIA_ROOT = root('media')
STATIC_ROOT = root('collected_static')
STATICFILES_DIRS = (
    root('assets'),
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (root('templates'),)
    },
]
~~~

- 패스트캠퍼스에서 배웠던 settings.py 작성 방법을 잠깐 보도록 하겠습니다.
- 궁금한점 : secrets 파일은 어떻게 공유를 하나??