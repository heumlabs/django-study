# 19. Django Admin 이용하기

- Django 프레임워크의 큰 장점 중 하나

## 19.1 Admin 기능은 최종 사용자를 위한 것이 아니다.

- 사이트 관리 작업 차원에서 사이트 관리자에게 데이터를 추가, 수정, 삭제할 수 있는 권한을 제공하는 것
- 물론 최종 사용자를 위한 기능으로까지 확장될 수 있지만 권장하지 않는다.

## 19.2 Admin 커스터마이징 vs. 새로운 Views

- Admin을 커스터마이징 하는 것보다 목적에 부합하는 단순한 View를 만드는 것이 수고를 덜 한다.

## 19.3 객체의 이름(문자열 표현) 보여 주기

- 객체를 표현하는(보여주는) 더 좋은 방법은 무엇이 있을까?

### 19.3.1 `__str__()` 사용하기

### 19.3.2 `list_display` 사용하기

- 문자열 표현(`__str__()`)방식외에 `list_display`도 사용할 수 있다.

```python
from django.contrib import admin
from .models import IceCreamBar

@admin.register(IceCreamBar)
class IceCreamBarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'shell', 'filling')
```

## 19.4 ModelAdmin 클래스에 호출자 추가하기

- Django ModelAdmin에 호출 가능한 method나 function을 추가할 수 있다.

```python
# icecreambars/admin.py
from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html
from .models import IceCreamBar

@admin.register(IceCreamBar)
class IceCreamBarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'shell', 'filling')
    readonly_fields = ('show_url',)
    
    def show_url(self, instance):
        url = reverse('ice_cream_bar_detail', kwargs={'pk': instance.pk})
        response = format_html("""<a href="{0}">{0}</a>""", url)
        return response
    
    show_url.short_description = 'Ice Cream Bar URL'
    # HTML 태그 보여주기 (사용자 입력 데이터에 allow_tags의 값을 절대 True로 하지 말 것!)
    show_url.allow_tags = True
```

- [초보몽키의 'get_absolute_url()' 에 대해서 알아보기](https://wayhome25.github.io/django/2017/05/05/django-url-reverse/)


## 19.5 여러 사용자가 이용하는 환경에서의 복잡함을 인지해라.

- Django admin에는 Lock을 거는 기능이 없다.
- 그래서 동시에 똑같은 데이터를 수정 할 경우 그냥 덮어 씌운다.

## 19.6 Django's Admin 문서 생성기

- django.contrib.admindocs 패키지
    - 23장에서 다루는 도구들 보다 이전에 만들어진 패키지이지만 여전히 유용하다.
    - 모델, 뷰, 커스텀 템플릿 태그, 커스텀 필터 등 프로젝트 컴포넌트의 docstring을 보여주기 때문에 프로젝트 리뷰 차원에서 유용
    - [로컬에 설정한 admindocs 살펴보기](http://localhost:8000/admin/doc/)
    
- jango.contrib.admindocs 사용방법
    1. pip install docutils 실행
    2. INSTALLED_APPS에 django.contrib.admindocs 추가
    3. 루트 URLConf에 `(r'^admin/doc/', include('django.contrib.admindocs.urls'))` 추가

## 19.7 Django Admin에 커스텀 스킨 이용하기

- 일반적으로 잘 알려진 django.contrib.admin 스킨
    - django-grappelli
    - django-suit
    - django-admin-bootstrapped
    - [좀 더 다양한 스킨 보기](https://djangopackages.org/grids/g/admin-styling/)

- Django Admin 의 커스텀 스킨을 만드는 것은 쉬운것이 아니다.

- 다음 세부 chapter에 스킨을 커스터마이징하는 데 필요한 팁을 확인해보자

### 19.7.1 평가 포인트: 문서화가 전부다

- 이미 개발된 스킨을 프로젝트에 추가하는 것은 쉽지만 향후에 유지보수가 어려워질 수 있다.
- 그러므로 문서화를 잘 하자

### 19.7.2 이용하는 모든 Admin Extensions에 대한 TestCase를 작성해라

- 기본으로 제공되는 django.contrib.admin에서는 잘 작동하던 기능들이 커스텀 스킨에서는 깨지거나 제대로 작동하지 않을 수 있다.
- 그러므로 Django Admin에 대한 TestCase 작성하자
- 테스팅에 대한 것은 Chapter22 를 참고

## 19.8 Django Admin 보안

- 당연한 이야기이지만 Django Admin의 보안은 매우 중요하다.

### 19.8.1 기본 Admin URL을 바꿔라

- `yoursite.com/admin/` 으로 되어 있는 주소를 길고, 어려운 것으로 바꾸자.

### 19.8.2 django-admin-honeypot을 사용해라

- django-admin-honeypot은 가짜 admin 페이지를 제공하여 여기에 접근하려는 사람의 로그인 정보를 알 수 있다.
- [django-admin-honeypot GitHub](https://github.com/dmpayton/django-admin-honeypot)

### 19.8.3 HTTPS를 통해서만 접근하도록 하자

- HTTP 접속을 허용되어 있다면 좀 더 보안이 필요하다

- TLS 보안이 필요하다 (Chapter 26.6 : HTTPS Everywhere 참고)

### 19.8.4 IP로 Admin 접근을 제한하자

- Django Admin에 특정 IP 주소에 대한 액세스 만 허용하도록 웹 서버를 구성하자.

- 웹 서버 단계(예: Nginx)에서 분리하는 것이 좋다

## 19.9 Admin docs의 보안

- 위에서 언급한 Django Admin의 보안 방법과 동일하게 관리가 되어야 한다.

    - URL 주소 바꾸기
    - HTTPS를 통해서만 접근 허용하기
    - 접근 가능한 IP 설정
