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
