# 33. 디버깅의 기술

## 33.1 개발 환경에서의 디버깅

### 33.1.1 django-debug-toolbar 이용하기

- https://pypi.python.org/pypi/django-debug-toolbar
- https://django-debug-toolbar.readthedocs.org

### 33.1.2 짜증나는 클래스 기반 뷰 에러

`as_view()` 메서드를 잊어버린 경우 TypeError가 발생한다.

```python
# 잘못된 코드
url(r'^$',  HomePageView, name='home'),

# 수정된 코드
url(r'^$',  HomePageView.as_view(), name='home'),
```

### 33.1.3 파이썬 디버거 마스터하기

`PDB`라고도 ㅜ불리는 파이썬 디버거는 지정된 중단점에서 소스 코드와 상호 연동이 가능한 발전된 REPL을 제공한다.

다음 세 가지의 경우에 PDB를 이용한다

1. 테스트 케이스 안에서
2. 개발 환경에서 HTTP 요청 중에 중단점을 설정하면 요청 처리를 개발자의 페이스에 맞게 추적하는 데 도움이 된다.
3. management command를 디버깅하기 위해

> ##### 배포 이전에 PDB가 코드에 남아 있는지 확인하자.
>
> PDB의 중단점을 코드에 남겨놓은 상태에서 상용으로 배포하면 사용자의 요청을 다 처리하기도 전에 해당 프로세스가 멈추는 장애를 일으키게 된다.  
> 배포하기 전에 pdb를 가진 코드를 검색해야 하며 flake8 같은 도구를 이용하여 자동으로 pdb의 존재를 확인해야 한다..

#####  참고 자료

- Python’s pdb documentation: docs.python.org/3/library/pdb.html
- Using PDB with Django: /mike.tig.as/blog/2010/09/14/pdb/

##### 패키지들

- IPDB: pypi.python.org/pypi/ipdb
- Using IPDB with pytest pypi.python.org/pypi/pytest-ipdb


### 33.1.4 Form File Upload의 핵심 기억하기

파일 업로드에서 문제가 발생한 경우 다음을 확인한다.

1. `<form>` 태그에 인코딩 타입이 포함되어 있는가?

    ```html
    <form action="{% url 'stores:file_upload' store.pk %}"
        method="post"
        enctype="multipart/form-data">
    ```

2. 함수 기반 뷰에서 뷰가 request.FILES를 처리하고 있는가?(예제코드는 책을 참조)
    
    > ##### Form-Based Class Based Generic Views
    >
    > 뷰가 다음 중 하나로부터 상속되었다면 request.FILES가 뷰 코드 안에 들어있는지 걱정하지 않아도 된다.
    > - django.views.generic.edit.FormMixin
    > - django.views.generic.edit.FormView
    > - django.views.generic.edit.CreateView
    > -django.views.generic.edit.UpdateView

### 33.1.5 텍스트 편집기나 IDE의 힘을 빌리기

Sublime Text, Textmates, Vim, Emacs 등 여러 편집기 중 하나를 사용한다면 파이썬과 장고에 특화된 옵션이나 플러그인을 찾아 이용하기를 바란다.

Pycharm, PyDev, WingIDE, Komodo 등 IDE를 이용한다면 해당 IDE에 파이썬과 장고에 특화된 기능이 내장되어 있고 활성화 되어 있을 것이다. IDE의 모든 기능을 이용하지 않고 있다면 반드시 해당 기능을 비롯하여 IDE의 전 기능을 이용하기 바란다.

> ##### 최고의 IDE 또는 텍스트 편집기는 무엇인가?
>
> "자신이 선호하는 것이 바로 최고다."

## 33.2 상용 서비스 시스템의 디버깅

### 33.2.1 로그를 좀 더 편하게 읽기

상용 시스템 로그 파일을 분석할 때의 문제점: 로그 크기가 너무 방대해 원인을 파악하기 힘듦

-> Sentry 등의 로그 분석 시스템을 이용한다.

### 33.2.2 상용 환경 미러링

상용 환경을 복제할 때 다음 절차를 따른다.

1. 방화벽이나 보안체계 안쪽에 상용 환경과 동일한 원격 서버를 세팅한다.
2. 상용 환경의 데이터를 복사해 온다. (개인 정보에 관련된 데이터에 주의)
3. 상용 환경 미러링 시스템에 접근이 필요한 사람에게 shell 접근을 허용한다.

### 33.2.3 UserBasedExceptionMiddleware

`settings.DEBUG = True`의 500 페이지를 특별한 슈퍼 사용자에게만 제공할 수 있다면 어떨까?

```python
# core/middleware.py
import sys

from django.views.debug import technical_500_response

class UserBasedExceptionMiddleware:
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
```

### 33.2.4 고질적인 settings.ALLOWED\_HOSTS 에러

어떨때 ALLOWED\_HOSTs 에러가 발생할까?

1. `settings.DEBUG=False`
2. ALLOWED\_HOSTS에 있는 호스트/도메인 이름에 매치되는 요청을 찾을 수 없는 경우  
    (e.g. ALLOWED\_HOSTS가 빈 리스트인데, example.com으로 페이지를 요청한 경우)
3. Django는 뭔가 의심스러운 일이 벌어지고 있다고 판단하여 SuspiciousOperation 에러를 발생시킨다.

- https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts

## 33.3 기능 설정

상용서버의 모든 사용자에게 푸시되기 전에 일부 사용자에게만 새로운 기능을 먼저 제공한다면 어떨까? 기능 설정이 바로 이것이다.

### 33.3.1 기능 설정 패키지

- https://github.com/disqus/gargoyle
- https://github.com/django-waffle/django-waffle

### 33.3.2 기능 설정과 단위 테스트

기능 설정의 한 가지 단점은 기능 설정에 의해 그 기능의 해당 코드에 대한 테스트가 비활성화 될 수 있다는 것이다. 이에 대한 해답은 해당 기능이 켜지거나 꺼졌어도 두 가지 경우에 대해 전부 테스트되게 하는 것이다.

그것을 위해서 장고 테스팅 프레임워크 내에서 기능 설정을 끄고 켜는 방법을 알아 둘 필요가 있다.

- https://gargoyle.readthedocs.io/en/latest/usage/index.html#testing-switches
- http://waffle.readthedocs.io/en/latest/testing/automated.html#testing-automated
