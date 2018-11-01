# 16. Django REST Framework로 REST API 구현하기

- REST API: Representational State Transfer Application Programming Interface
- Django REST Framework(DRF) : Django에서 REST API를 구축할 수 있게 도와줌
  - 2013년부터 시작한 (API가 있는) Djagno 프로젝트의 90~95%는 DRF를 사용
- 공식문서 Link
  - http://www.django-rest-framework.org/tutorial/quickstart/
  - http://www.django-rest-framework.org/tutorial/1-serialization/


## 16.1 기본 REST API 디자인의 핵심

- REST API 설계 시 각 요청의 유형에 알맞는 HTTP Method를 사용하면 됨 (Table 16.2 참고)
  - 읽기 전용 API : GET Method만
  - 읽기-쓰기 API : GET, POST, PUT, DELETE Method
  - 모든 작업을 GET, POST에만 의존하는 것은 API 사용자에게는 좌절스러운 패턴일 수 있음
  - GET, PUT, DELETE 멱등성(idempotent). POST, PATCH는 X
  - PATCH는 잘 구현하지 않지만 PUT 요청을 지원하는 API라면 구현하는 것이 좋음
- REST API의 응답 시 적절한 의미를 가지는 HTTP Status Code를 사용 (Table 16.2 참고)

## 16.2 Illustrating Design Concepts With a Simple API

간단한 JSON API 구현 예제 (`flavors` app)

- AdminUser만 허용하도록 기본값 설정
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_PERMISSION_CLASSES': (
          'rest_framework.permissions.IsAdminUser',
      ),
  }
  ```

- Model
  - Sequential Key를 공식 식별자로 사용하지 마라
    - 보안문제. 교재에서는 UUID 필드를 사용함.

  ```python
    # flavors/models.py
  import uuid as uuid_lib

  from django.db import models
  from django.urls import reverse

    class Flavor(models.Model):
        title = models.CharField(max_length=255)
        slug = models.SlugField(unique=True) # Used to find the web URL
        uuid = models.UUIDField( # Used by the API to look up the record
              db_index=True,
              default=uuid_lib.uuid4,
              editable=False)
        scoops_remaining = models.IntegerField(default=0)

      def get_absolute_url(self):
          return reverse('flavors:detail', kwargs={'slug': self.slug})
  ```

- Serializer
```python
# flavors/api/serializers.py
from rest_framework import serializers

from ..models import Flavor

class FlavorSerializer(serializers.ModelSerializer):          class Meta:
        model = Flavor
        fields = ['title', 'slug', 'uuid', 'scoops_remaining']
```

- View
  - http://cdrf.co
```python
# flavors/api/views.py
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from ..models import Flavor
from .serializers import FlavorSerializer

class FlavorListCreateAPIView(ListCreateAPIView):    
    queryset = Flavor.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = FlavorSerializer
    lookup_field = 'uuid'  # Don't use Flavor.id!

class FlavorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Flavor.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = FlavorSerializer
    lookup_field = 'uuid'  # Don't use Flavor.id!
```

- URL
```python
# flavors/urls.py
from django.conf.urls import url

from flavors.api import views

urlpatterns = [
    # /flavors/api/
    url(
        regex=r'^api/$',
        view=views.FlavorListCreateAPIView.as_view(),
        name='flavor_rest_api'
    ),
    # /flavors/api/:slug/
    url(
        regex=r'^api/(?P<uuid>[-\w]+)/$',
        view=views.FlavorRetrieveUpdateDestroyAPIView.as_view(),
        name='flavor_rest_api'
    )
]
```

- 적절한 Permission을 사용해야함
  - http://www.django-rest-framework.org/api-guide/authentication/
  - http://www.django-rest-framework.org/api-guide/permissions/

- REST API의 URL을 표현할 때 변수는 `:uuid` 형식을 주로 씀
```
flavors/api/
flavors/api/:uuid/
```

## 16.3 REST API 구조

### 16.3.1 일관된 API 모듈 이름 사용

- 모든 API 컴포넌트를 각 app폴더 하위의 `api`폴더 하위에 위치
  - root에 놓게되면 너무 커짐
- 라우터는 urls.py에 그대로 위치

```bash
flavors/
├── api/
│   ├── __init__.py
│   ├── authentication.py
│   ├── parsers.py
│   ├── permissions.py
│   ├── renderers.py
│   ├── serializers.py
│   ├── validators.py
│   ├── views.py
│   ├── viewsets.py # 자체 모듈
```

### 16.3.2 프로젝트 코드들은 간결하게 정리되어 있어야 한다

- 상호 연결되는 앱이 많은 프로젝트의 경우 특정 API View의 위치를 찾기 어려울 수 있음
- 이런 경우 API 전용앱을 만드는 것이 더 적절할 수 있음 (serializer, renderer, view 포함)
- 앱의 이름은 버전을 반영해야 함 (ex. `apiv4`)
- 하지만 이 앱이 너무 커지면 앱과의 연결이 끊어질 수 있음

### 16.3.3 앱의 코드는 앱 안에 두자

- View 클래스의 갯수가 많아져 하나의 views.py 혹은 viewsets.py 모듈에서 찾기가 힘든 경우 나눌 수 있다. 하지만 상호 연결되는 작은 앱이 많을 경우 마찬가지로 수 많은 API 컴포넌트들의 위치를 찾는 것이 힘들 수 있음.

### 16.3.4 비즈니스 로직은 API View 밖에서

- 일반 Django View와 마찬가지 이유. (Section 8.5 참고)

### 16.3.5 API URL들을 모아두기

- 프로젝트 전반에 걸쳐 사용하는 API의 경우 `core/api_url.py` 혹은 `core/apiv1_urls.py`로 URLConf 파일을 만들어서 모아서 관리
- 아래 예시는 "여러 앱의 API 뷰를 하나로 모은" 예제이다.
```python
# core/api_urls.py
"""Called from the project root's urls.py URLConf thus:
        url(r'^api/', include('core.api_urls', namespace='api')),
"""
from django.conf.urls import url

from flavors.api import views as flavor_views
from users.api import views as user_views


urlpatterns = [
    # {% url 'api:flavors' %}
    url(
        regex=r'^flavors/$',
        view=flavor_views.FlavorCreateReadView.as_view(),
        name='flavors'
    ),
    # {% url 'api:flavors' flavor.uuid %}
    url(
        regex=r'^flavors/(?P<uuid>[-\w]+)/$',
        view=flavor_views.FlavorReadUpdateDeleteView.as_view(),
        name='flavors'
    ),
    # {% url 'api:users' %}
    url(
        regex=r'^users/$',
        view=user_views.UserCreateReadView.as_view(),
        name='users'
    ),
    # {% url 'api:users' user.uuid %}
           url(
           regex=r'^users/(?P<uuid>[-\w]+)/$',
           view=user_views.UserReadUpdateDeleteView.as_view(),
           name='users'
    ),
]
```

### 16.3.6 API 테스트하기

- 쉽게 할 수 있음. Chapter 22에서 다룰 것임!

### 16.3.7 API 버전 관리하기

- `api/v1/flavors`, `api/v2/users`
- 버전이 바뀌었을 때 사용자들이 이전 버전을 사용할 수 있게 해야함
- 사용자들을 위해 이전 버전의 중지를 미리 공지해야함

### 16.3.8 Customized 인증은 조심해서!

- 유의 사항
  - 간단하게
  - 테스트
  - 기존 표준 인증 체계가 왜 적합하지 않은지 문서화
  - 인증체계가 어떻게 설계되었는지 자세히 문서화
  - 비 쿠키 기반 체계가 아니라면, CSRF를 비활성화 하지 마라


## 16.4 When DRF Gets in the Way

- DRF는 강력하지만 추상화가 많아 어렵게 느껴진다. 아래 내용을 같이 보면서 극복해보자.

### 16.4.1 원격 프로시져 호출 vs REST APIs

- REST APIs는 데이터 접근에 용이하지만, 리소스는 프로그램 설계와 항상 같지 않다.
- 예를 들어 시럽과 아이스크림(sundae)을 두 가지 리소스로 표현하기는 쉽지만 시럽을 아이스크림에 붓는 행위는 쉽지 않다.
- REST APIs의 일부분으로 클라이언트에 sundae.pour_syrup(syrup)과 같은 메소드를 제공하는 것이 가능하다.
- sundae.pour_syrup(syrup)은 원격 프로시져 호출로 분류된다.
- DRF에서 제공하는 view 대신 기본 APIView를 사용한다(아래 예시 참고)

```python
# sundaes/api/views.py
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Sundae, Syrup
from .serializers import SundaeSerializer, SyrupSerializer

class PourSyrupOnSundaeView(APIView):
    """View dedicated to adding syrup to sundaes"""
    def post(self, request, *args, **kwargs):
        # Process pouring of syrup here,
        # Limit each type of syrup to just one pour
        # Max pours is 3 per sundae
        sundae = get_object_or_404(Sundae, uuid=request.data['uuid'])
        try:
            sundae.add_syrup(request.data['syrup'])
        except Sundae.TooManySyrups:
            msg = "Sundae already maxed out for syrups"
              return Response({'message': msg}, status_code=400)
        except Syrup.DoesNotExist
            msg = "{} does not exist".format(request.data['syrup'])
            return Response({'message': msg}, status_code=404)
        return Response(SundaeSerializer(sundae).data)

    def get(self, request, *args, **kwargs)
        # Get list of syrups already poured onto the sundae
        sundae = get_object_or_404(Sundae, uuid=request.data['uuid'])
        syrups = [SyrupSerializer(x).data for x in sundae.syrup_set.all()]
        return Response(syrups)
```

```python
/sundae/  # GET, POST
/sundae/:uuid/  # PUT, DELETE
/sundae/:uuid/syrup/  # GET, POST
/syrup/  # GET, POST
/syrup/:uuid/  # PUT, DELETE
```

### 16.4.2 복잡한 데이터의 문제점

- 콘과 아이스크림의 모델이 각각 존재한다고 가정하자. 그런데 콘에는 Scoop이 포함되어 있다.
- Scoop을 여러개 추가할 때는 어떻게 해야 할까? 아래 url 구조를 확인해보자.
- (회사와 피고용자의 관계와 유사??)

```python
/api/cones/  # GET, POST
/api/cones/:uuid/  # PUT, DELETE
/api/cones/:uuid/scoops/  # GET, POST
/api/cones/:uuid/scoops/:uuid/  # PUT, DELETE
/api/scoops/  # GET, POST
/api/scoops/:uuid/  # PUT, DELETE
```

### 16.4.3 Simplify! Go Atomic!

- 본질적인 DRF 관련 문제가 발생하면 다음의 질문을 참고
    - 뷰를 단순화 할 수 있을까? APIView로 전환하면 해결되나?
    - REST 데이터 모델을 단순화 할 수 있을까? 더 많은 뷰를 추가하면 해결되나?
    - serializer가 너무 복잡한 경우, 같은 모델에 대해 두 개의 서로 다른 serializer로 나눌까?

- DRF의 문제를 극복하기 위해 API를 더 작고 원자적(atomic)인 구성 요소로 나누는 것이 좋다.
- Atomic-style components의 이점은 아래와 같다.
    - 구성요소가 적으므로 빠르고 쉽게 문서화가 가능하다
    - 코드 분기가 적어서 테스트가 쉽다
    - chokepoints가 더 고립되어 있기 때문에 병목 현상을 쉽게 해결할 수 있다(?)
    - 뷰 단위로 액세스를 쉽게 변경할 수 있기 때문에 보안이 향상된다

## 16.5 외부 API 중단하기

### 16.5.1 1단계: 사용자들에게 서비스 중지 예고하기

- 6개월 정도의 기간이 적당하며, 최소 한 달 전에는 공지를 해야한다

### 16.5.2 2단계: 410 에러뷰로 API 교체하기

- 최종적으로 API가 중지되면 아래와 같은 내용이 포함된 간단한 410 에러뷰를 서비스한다.
    - 새로운 API 링크
    - 새로운 API 문서의 링크
    - 서비스 중지에 대한 세부 사항을 알려주는 문서의 링크

## 16.6 API 접속 제한하기

- 접속 제한은 한 사용자가 주어진 시간에 얼마 이상의 요청을 보낼 때 이를 제어하는 것을 말한다.

### 16.6.1 제한 없는 API는 위험하다

- 애플리케이션에 장애를 일으킬 수 있다. (GitHub API 사례)

### 16.6.2 REST 프레임워크는 반드시 접속 제한을 해야만 한다

### 16.6.3 비즈니스 계획으로서의 접속 제한

- 접근 수준(시간당 횟수)에 따라 가격정책을 다양하게 수립

## 16.7 자신의 REST API 알리기

### 16.7.1 문서

- 읽기 쉽고 잘 이해가 되도록 작성
- 쉽게 이용이 가능한 샘플 코드도 추가
- 23장에서 더 알아보자

### 16.7.2 클라이언트 SDK 제공하기

- 여러 언어를 지원하는 SDK를 제공하자. 많을 수록 좋다
- 21.9장에서 SDK 만들기에 대한 관련된 내용이 있으니 참고하자
