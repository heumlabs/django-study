# 5. settings와 requirements 파일

- Django 1.11은 settings 모듈에서 150가지가 넘는 setting을 조정할 수 있음
- Setting 값은 서버가 시작할 때 로드되며, 서버 재시작 말고는 운영 중일때 setting을 바꾸지 않는다.
- 주요 Tip
  - 모든 Setting 값은 버전 관리가 되어야 함
  - 반복되는 내용은 Base Setting에서 상속 (복붙금지)
  - Secret Key들은 VCS에서 제외

## 5.1 버전 관리되지 않는 Local Settings은 피한다.

- `SECRET_KEY`, `아마존 API 키` 등을 저장소에서 제외해야 함

- 버전 관리되지 않는 Local Settings 파일이 존재할 시 문제점
  - 모든 Machine에 Untracked Code 존재
  - Local에서 Production 환경의 버그 재현 불가
  - local_settings를 모두가 복사/붙여넣기 해야함 (`Dont Repeat Tourself`)

- 환경 별 Settings 파일을 공통된 객체에서 상속받아 VCS에서 관리해야 함

## 5.2 여러 개의 Settings 파일 사용하기

```bash
settings/
├── __init__.py
├── base.py
├── local.py
├── staging.py
├── test.py
├── production.py
├── ci.py
```

- *Each settings module should have its own corresponding requirements file*
- `--settings=twoscoops.settings.lo
- 유일하게 import * 구문을 이용해도 됨
- 개발자 별 세팅 파일 : `local_audreyr.py`

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