# 22. 테스트, 정말 거추장스럽고 낭비일까?

## 22.1 돈, 직장, 심지어 생명과도 연과되어 있는 테스팅

- 높은 수준의 품질을 요구하는 경우

    - 의료 정보와 이에 관련된 업무를 처리하는 애플리케이션
    - 사람들의 생명에 연관된 리소스를 제공하는 애플리케이션
    - 사람들의 돈에 관련된 업무를 처리하거나 처리할 애플리케이션
    
- `coverage` 라이브러리는 django 프로젝트 테스팅에 매우 유용하다.
이 도구는 코드의 어떤 부분이 테스트되었고, 어떤 라인들이 테스트되지 않았는지 보여준다.
또한 퍼센트로 보여주어 편한다.

## 22.2 어떻게 테스트를 구축할 것인가

```text
popsicles/
    __init__.py
    admin.py
    forms.py
    models.py
    tests/
        __init__.py
        test_forms.py
        test_models.py
        test_views.py
    views.py
```

- 테스트 모듈에 test_ 접두어를 붙이지 않으면 django의 테스트 runner가 해당 테스트 파일을 인지하지 못한다.

## 22.3 단위 테스트 작성하기

### 22.3.1 각 테스트 메서드는 테스트를 한 가지씩 수행해야 한다

- 테스트 메서드는 그 테스트 범위가 좁아야 한다.
- 하나의 단위 테스트는 절대로 여러 개의 뷰나 모델, 폼 또는 한 클래스 안의 여러 메서드에 대한 테스트를 수행해서는 안된다.
- 하나의 테스트는 단 하나의 기능에 대해서만 테스트가 이루어져야 한다.(뷰면 뷰, 모델이면 모델)

- 뷰에 대한 테스트만을 딱 잘라서 하나의 테스트로 할 수 있을까? 아래는 테스트에 대한 환경을 최소한으로 구성하는 예이다.
```python
# flavors/tests/test_api.py
import json
from django.test import TestCase
from django.urls import reverse
from flavors.models import Flavor

class FlavorAPITests(TestCase):
    def setUp(self):
        Flavor.objects.get_or_create(title='A Title', slug='a-slug')

    def test_list(self):
        url = reverse('flavor_object_api')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
```

- 좀 더 확장된 예제이다.
```python
# flavors/tests/test_api.py
import json
from django.test import TestCase
from django.urls import reverse
from flavors.models import Flavor

class DjangoRestFrameworkTests(TestCase):
    def setUp(self):
        Flavor.objects.get_or_create(title='title1', slug='slug1')
        Flavor.objects.get_or_create(title='title2', slug='slug2')
        self.create_read_url = reverse('flavor_rest_api')
        self.read_update_delete_url = reverse('flavor_rest_api', kwargs={'slug': 'slug1'})
    
    def test_list(self):
        response = self.client.get(self.create_read_url)
        # Are both titles in the content?
        self.assertContains(response, 'title1')
        self.assertContains(response, 'title2')
    
    def test_detail(self):
        response = self.client.get(self.read_update_delete_url)
        data = json.loads(response.content)
        content = {'id': 1, 'title': 'title1', 'slug': 'slug1', 'scoops_remaining': 0}
        self.assertEquals(data, content)

    def test_create(self):
        post = {'title': 'title3', 'slug': 'slug3'}
        response = self.client.post(self.create_read_url, post)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 201)
        content = {'id': 3, 'title': 'title3', 'slug': 'slug3', 'scoops_remaining': 0}
        self.assertEquals(data, content)
        self.assertEquals(Flavor.objects.count(), 3)
    
    def test_delete(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Flavor.objects.count(), 1)

```

### 22.3.2 뷰에 대해서는 가능하면 Request Factory를 이용하자

- [django.test.client.RequestFactory](https://docs.djangoproject.com/ko/2.1/topics/testing/advanced/)
는 모든 뷰에 대해 해당 뷰의 첫 번째 인자로 이용할 수 있는 request 인스턴스를 제공한다.
이는 일반 장고 테스트 클라이언트보다 독립된 환경을 제공한다.

- 테스트하고자 하는 뷰가 세션을 필요로 할 때는 다음과 같이 작성한다.
```python
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from .views import cheese_flavors

def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request

def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request

class SavoryIceCreamTest(TestCase):
    def setUp(self):
        # 모든 테스트에서 이 요청 팩토리로 접근할 수 있어야 한다.
        self.factory = RequestFactory()
    
    def test_cheese_flavors(self):
        request = self.factory.get('/cheesy/broccoli/')
        request.user = AnonymousUser()
        # 요청 객체에 세션을 가지고 표식을 달도록 한다.
        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()
        # 요청에 대한 처리와 테스트를 진행한다.
        response = cheese_flavors(request)
        self.assertContains(response, 'bleah!')

```

### 22.3.3 테스트가 필요한 테스트 코드를 작성하지 말자

- 테스트는 가능한 한 단순하게 작성해야 한다.
- 테스트 케이스 안의 코드가 복잡하거나 추상적이라면 문제가 있다.

### 22.3.4 '같은 일을 반복하지 말라'는 법칙은 테스트 케이스를 작성할 때는 적용되지 않는다.

- setUp() 메서드는 테스트 클래스의 모든 테스트 메서드에 대해 재사용이 가능한 데이터를 만드는 데 도움이 된다.
- 비슷한 케이스를 각각 작성하는 것 대신 모든 경우를 만족시키는 하나의 메서드는 더 큰 어려움을 초래한다.

### 22.3.5 픽스처(Fixture)를 너무 신뢰하지 말자

- [What is Fixture??](https://twpower.github.io/20-how-to-use-fixture-in-django)
- 픽스처를 이용하면 더 큰 문제가 발생할 수 있다.
- 픽스처 대신 ORM에 의존하는 코드가 더 쉽다.
- 서드 파티 패키지를 이용할 수도 있다.
    - **[테스트 데이터를 생성해 주는 몇 가지 도구]**
    - factory boy: 모델 테스트 데이터를 생성해 주는 패키지
    - model mommy: 또 하나의 모델 테스트 데이터를 생성해 주는 패키지
    - mock: django뿐만 아니라 다른 환경에서도 이용 가능한 시스템의 일부를 대체할 수 있는 mock 객체를 생성해준다.
    python 3.3부터는 표준 라이브러리로 채택되었다.

### 22.3.6 테스트해야 할 대상들

- 물론 ***전부 다*** 테스트 해야한다. 아래 항목을 포함해서...

    - **뷰**: 데이터 뷰, 데이터 변경 그리고 커스텀 클래스에 기반을 둔 뷰 메서드
    - **모델**: 모델의 생성, 수정, 삭제 및 모델의 메서드와 모델 관리 메서드
    - **폼**: 폼 메서드, clean() 메서드, 커스텀 필드
    - **유효성 검사기**: 본인이 제작한 커스텀 유효성 검사기에 대해 다양한 테스트 케이스를 심도 깊게 작성하라.
    - **시그널**: 시그널은 원격에서 작동하기에 테스트를 하지 않을 경우 문제를 야기하기 쉽다.
    - **필터**: 필터들은 기본적으로 한 개 또는 두 개의 인자를 넘겨받는 함수이기 때문에 테스트를 제작하기에 그리 어렵지 않다.
    - **템플릿 태그**: 템플릿 태그는 그 기능이 막강하고 또한 템플릿 콘텍스트를 허용하기 때문에 테스트 케이스를 작성하는 것이 까다롭다. 이는 즉 정말 테스트해야할 대상이라는 것이다.
    - **기타**: 콘텍스트 프로세서, 미들웨어, 이메일, 그리고 이 목록에 포함되지 않은 모든 것
    - **실패**: 만약 위의 경우 중 어느 하나라도 실패하면 어떻게 될까?

### 22.3.7 실패를 위한 테스트 (테스트의 목적은 실패를 찾는 것이다.)

- 테스트 시나리오보다 예외적인 경우에 대한 테스트가 더욱 중요
- 성공 시나리오에서의 실패는 사용자에게 불편을 야기하지만,
- 실패 시나리오에서의 실패는 보안상의 문제점을 만들어 낼 수 있다.

- [python 공식문서: assertRaise](https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertRaises) 
- [pytest 문서: assertion](https://docs.pytest.org/en/latest/assert.html#assertions-about-expected-exceptions)

### 22.3.8 목(mock)을 이용하여 실제 데이터에 문제를 일이키지 않고 단위 테스트 하기

- 단위 테스트 중에는 외부 api에 대한 접속이나 이메일 수신, 웹훅으 비롯한 테스트 외적인 환경에 대한 액션이 이루어져서는 안된다.
- 그래서 외부 api를 이용하는 기능들에 대한 단위 테스트에 큰 난제이다.
- 이와 같은 경우 아래 두가지 방법을 이용해 보자.
    1. 단위 테스트 자체를 통합 테스트(Integeration Test)로 변경한다.
    2. 목(mock) 라이브러리를 이용하여 외부 api에 대한 가짜 응답(response)을 만든다.
- 목(mock) 라이브러리는 우리가 테스트를 위한 특정 값들의 반환을 필요로 할 때
매우 빠르게 이용할 수 있는 멍키 패치(monkey-patch) 라이브러리를 제공한다.

> **Monkey Patch**란 런타임에 메서드나 변수를 추가하거나 변경하는 것을 의미한다.

- 아래 예제는 아이스크림 api 라이브러리에 멍키 패치 방식을 적용한 예이다.
```python
from unittest import mock, TestCase
import icecreamapi
from flavors.exceptions import CantListFlavors
from flavors.utils import list_flavors_sorted

class TestIceCreamSorting(TestCase):
    # icecreamapi.get_flavors()의 멍키 패치 세팅
    @mock.patch.object(icecreamapi, 'get_flavors')
    def test_flavor_sort(self, get_flavors):
        # icecreamapi.get_flavors()가 정렬되어 있지 않는 리스트를 생성하도록 설정
        get_flavors.return_value = ['chocolate', 'vanilla', 'strawberry', ]
        
        # list_flavors_sorted()가 icecreamapi.get_flavors() 함수를 호출
        # 멍키 패치를 했으므로 항상 반환되는 값은 ['chocolate', 'strawberry', 'vanilla', ]가 되며
        # 이는 list_flavors_sorted()에 의해 자동으로 정렬된다.
        flavors = list_flavors_sorted()
        self.assertEqual(
            flavors,
            ['chocolate', 'strawberry', 'vanilla', ]
        )
```

### 22.3.9 좀 더 고급스러운 단언 메서드(Assertion Methods) 사용하기

- 유용하게 사용할 수 있는 Assertsion Methods들 아래 링크에서 확인
- [python 공식문서](https://docs.python.org/3/library/unittest.html#assert-methods)
- [django 공식문서](https://docs.djangoproject.com/en/1.11/topics/testing/tools/#assertions)

### 22.3.10 각 테스트의 목적을 문서화하라

- docstring에 목적과 분석내용을 작성하는 것이 큰 도움이 된다.

## 22.4 통합 테스트(Integeration Test)란?

- 통합 테스트란 개별적인 소프트웨어 모듈이 하나의 그룹으로 조합되어 테스트 되는 것을 의미한다.
- 단위 테스트가 끝난 후에 행하는 것이 가장 이상적이다.

#### 통합 테스트 예시

- 어플리케이션이 브라우저에 잘 작동하는지 확인하는 셀레늄(Selenium) 테스트
- 서드 파티 API에 대한 가상 목(mock) 응답을 대신하는 실제 테스팅
- 외부로 나가는 요청에 대한 유효성 검사를 위해 [requestb.in](requestb.in)이나 http://httpbin.org 등과 연동하는 경우
- API가 기대하는 대로 잘 작동하는지 확인하기 위해 [runscope.com](https://www.runscope.com/)을 이용하는 경우

#### 통합 테스트 문제점

- 통합 테스트 세팅에 많은 시간이 소요될 수 있다.
- 통합 테스트는 시스템 전체를 테스트 하기 때문에 ***단위 테스트와 비교하면 테스트 속도가 느리다.***
- 통합 테스트로부터 반환된 에러의 경우, 에러 이면에 숨어 있는 에러의 원인을 찾기가 단위 테스트보다 어렵다.
- 단위 테스트에 비해 많은 주의를 요구하여 작은 변경으로도 전반에 문제가 나타날 수 있다.

#### 이러한 문제점에도 불구하고 통합 테스트는 유용하고 이용할 만한 가치가 있는 테스트이다.

## 22.5 지속적 통합

- 프로젝트 저장소에 새로운 코드가 commit 될 때마다 테스트를 실행하는 지속적 통합 서버를 세팅해라.
- '32장 Continuous Integeration' 참고


## 22.6 알 게 뭐람? 테스트할 시간이 어디 있다고!

- 호미로 막을 것을 가래로 막는다.

## 22.7 테스트 범위 게임

- 최대한 많은 범위의 테스트를 하는 게임을 해 보길 권장한다. 날마다 테스트 범위가 넓어질 때마다 이기는 것이고,
테스트 범위가 줄어들 때마다 지는 것이다.

## 22.8 테스트 범위 게임 세팅하기

- test coverage는 개발자와 고객, 고용자, 투자자에게 프로젝트의 상태를 보여주는 매우 유용한 도구이다.
- 서드 파티 라이브러리는 테스트 할 필요가 없다. 우리가 만든 앱만 테스트 하자.

### 22.8.1 Step 1: 테스트 작성하기

### 22.8.2 Step 2: 테스트 실행하기 그리고 커버리지 리포트 작성하기

- project root에서 다음을 실행
`$ coverage run manage.py test --settings=twoscoops.settings.test`

### 22.8.3 Step 3: 리포트 생성하기

- coverage.py를 이용한다.
- project root에서 다음을 실행
`coverage html --omit="admin.py"`
- coverage 실행한 후에 project root에 'htmlcov/'라는 새로운 디렉토리에 index.html에서 테스트 실행 결과를 확인 할 수 있다.

## 22.9 테스트 범위 게임 시작하기

- 이 게임의 한 가지 규칙이 있다.
`테스트 커버리지를 낮추는 그 어떤 커밋도 허용하지 않기`

- 날마다 테스트 커버리지(예:65%)가 조금이라도 올라갈 때마다 게임에서 승리하는 것이다.
- 한번에 급속도로 증가한 테스트 커버리지보다 날마다 조금씩 증가하는 테스트 커버리지가 더 좋다.

## 22.10 unitest의 대안

- 지금까지의 모든 예제는 unitest 라이브러리를 이용하였다.
- 너무 복잡한 절차를 필요로 하지 않는 대안이 몇 개 있다.

- [pytest-django](https://pypi.org/project/pytest-django/)
- [django-nose](https://pypi.org/project/django-nose/)

- pytest 예제
```python
# test_models.py
from pytest import raises
from cones.models import Cone

def test_good_choice():
    assert Cone.objects.filter(type='sugar').count() == 1
    
def test_bad_cone_choice():
    with raises(Cone.DoesNotExist):
        Cone.objects.get(type='spaghetti')
```
