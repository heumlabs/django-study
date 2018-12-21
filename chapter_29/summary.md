# 29. 유틸리티들에 대해

## 29.1 유틸리티들을 위한 Core App 만들기

- 프로젝트 전반에 걸쳐 쓰이는 함수들과 객체들은 코어(Core)라는 App에서 관리.
- common, generic, util, utils 란 이름으로 대체 가능
- Core App의 구조는 일반 Django 앱의 구성을 따르자. Core App의 구성 예제는 다음과 같다.

```
core/
    __init__.py
    managers.py  # custom model manager(s) 포함
    models.py
    views.py  # custom view mixin(s) 포함
```
- Core App의 임포트 예제

```python
from core.managers import PublishedManager
from core.views import IceCreamMixin
```

## 29.2 유틸리티 모듈을 이용하여 앱을 최적화하기

- utils.py와 helper.py가 왜 유용한지 같이 살펴보자

### 29.2.1 여러 곳에서 공통으로 쓰이는 코드를 저장해 두기

- 공통으로 쓰이는 함수와 클래스는 models.py, forms.py 등의 모듈에 넣기에 애매하므로 utils.py에 위치시키자.

### 29.2.2 모델을 좀 더 간결하게 만들기

- 많은 필드와 메서드로 인해 비대해진 A 모델은 유지보수가 쉽지 않다.
- 프로퍼티, 클래스 메서드 등 A/utils.py 안으로 넣을 수 있는 부분을 찾아서 캡슐화 하자.
그러면 코드를 분산시켜 재사용 및 테스팅이 수월해진다.

### 29.2.3 좀 더 손쉬운 테스팅

- 복잡한 로직을 독립적인 모듈로 분리하면 좀 더 쉬운 테스트가 가능해진다.

### 29.2.4 한 가지 기능에 집중하는 유틸리티 코드

- 함수나 클래스들에 여러 기능이나 동작을 넣지 말자.
- 각 유틸리티 함수는 각각 자기가 맡은 한 가지 기능만 수행하게 한다.
- 반복적인 작업이나 중복되는 기능을 피하자.
- 모델의 기능과 중복되는 유틸리티 함수를 만드는 것은 피하자.

## 29.3 Django 자체에 내장된 스우스 군용 칼(맥가이버 칼)

- Django는 유용한 헬퍼 함수를 django.utils 패키지에 내장하고 있다.
- (주의)이 패키지의 모듈들은 django 내부적인 이용을 목적으로 제작되었으며, **버전이 변경이 되면 그 용도와 내용이 바뀐다.**
- [Django 공식문서 - utils](https://docs.djangoproject.com/en/1.11/ref/utils/) 를 읽어보는 것을 추천

### 29.3.1 django.contrib.humanize

- 사용자에게 좀 더 **'인간' 친화적인 기능**들을 제공하는 **템플릿 필터**다.

| template filter | example |
|-----------------|---------|
| apnumber        |`1` becomes `one`|
| intcomma        |`4500000` becomes `4,500,000`|
| intword         |`1200000` becomes `1.2 million`|
| naturalday      |`08 May 2016` becomes `yesterday`|
| naturaltime     |`09 May 2016 20:54:31` becomes `29 seconds ago`|
| ordinal         |`3` becomes `3r`d|

- 참고 사이트 [Django Tips #2 humanize - Simple is Better Than Complex](https://simpleisbetterthancomplex.com/tips/2016/05/09/django-tip-2-humanize.html)
- [Django 공식문서](https://docs.djangoproject.com/en/2.1/ref/contrib/humanize/)

- 아래 예제와 같이 필터들을 함수로 따로 임포트해서 이용할 수도 있다.

```python
from django.contrib.humanize.templatetags.humanize import naturalday, intcomma

natural_day = naturalday(value1)
money = intcomma(value2)
```

### 29.3.2 django.utils.decorators.method_decorator(decorator)

- function 과 method 의 차이점? [Functions & Methods (함수와 메소드)](http://yusulism.tistory.com/11)
- 클래스의 메소드는 독립형 함수와 완전히 같지 않으므로 함수 데코레이터를 메소드에 적용 할 수는 없다.
이 때 method_decorator 를 이용하면 함수 데코레이터를 메소드 데코레이터로 변환하여 인스턴스 메소드에서 사용할 수 있다.

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class ProtectedView(TemplateView):
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)
```
- [django 공식문서](https://docs.djangoproject.com/en/1.11/ref/utils/#module-django.utils.decorators)

### 29.3.3 django.utils.decorators.decorator_from_middleware(middleware)

- decorator_from_middleware 메소드는 인자로 전달된 미들웨어 클래스 뷰 데코레이터를 반환한다.
이를 통해 뷰 단위로 미들웨어 기능을 사용할 수 있다. 매개 변수가 전달되지 않은 미들웨어가 생성된다.
- 인자가 필요한 경우에는 decorator_from_middleware_with_args 를 사용한다.

```python
cache_page = decorator_from_middleware_with_args(CacheMiddleware)

@cache_page(3600)
def my_view(request):
    pass
```

### 29.3.4 django.utils.encoding.force_text(value)

- 이 함수는 django의 무엇이든지 Python3에서는 str 으로, Python2에서는 unicode 형태로 변환시킨다.
- [django 공식문서](https://docs.djangoproject.com/en/1.11/ref/utils/#module-django.utils.encoding)

### 29.3.5 django.utils.functional.cached_property

- self 인자만을 단독으로 가진 메서드의 결과를 프로퍼티로 메모리에 캐시해 주는 기능을 한다.
- 해당 객체가 존재하는 동안 메서드의 값이 항상 일정한지 확인하는 용도로 쓰일 수 있다.
이는 외부 서드 파티 API 또는 데이터베이스 트랜잭션 관련 작업을 할 때 매우 유용하게 쓰인다.

```python
# the model
class Person(models.Model):

    def friends(self):
        # expensive computation
        pass
        return friends

# in the view:
if person.friends():
    pass
```
```python
from django.utils.functional import cached_property

class Person(models.Model):

    @cached_property
    def friends(self):
        pass
```

- 여기서 드는 의문점?? 그러면 @property 와 @cached_property 의 차이점은??
- @cached_property는 객체가 존재하는 한 값이 변경되지 않지만 refresh_from_db()메서드를 이용하면 @property는 변경된 값을 전달한다.
[Django: @cached_property on models](https://medium.com/@fdemmer/django-cached-property-on-models-f4673de33990)


### 29.3.6 django.utils.html.format_html(format_str, args, **kwargs)

- 이 메서드는 HTML을 처리하기 위해 제작된 것을 제외하고 str.format() 메서드와 비슷하다.

```python
format_html("{} <b>{}</b> {}",
    mark_safe(some_html),
    some_text,
    some_other_text,
)
```
[django 공식문서](https://docs.djangoproject.com/en/1.11/ref/utils/#module-django.utils.html)

### 29.3.7 django.utils.html_tags(value)

- 사용자에게 받은 콘텐츠에서 html 코드를 분리 할 때 사용한다. 태그 사이의 텍스트는 남기고 태그만 제거한다. 
- 보안상 안전하지 않을 수 있으므로 사용 시 주의를 요한다.

### 29.3.8 django.utils.six

- six 는 Python2 와 Python3의 호환 라이브러리이다.
- 다른 여러 프로젝트에서 독자적인 패키지 형태로 존재한다.

```python
# django.utils.six.string_types() 예제

def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        if isinstance(self.remote_field.model, six.string_types):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.remote_field.model))
```

### 29.3.9 django.utils.text.slugify(allow_unicode=False)

- allow_unicode가 False 일 경우 ASCII로 변환(기본값)
- 공백을 하이픈으로 변환
- 영숫자, 밑줄 또는 하이픈이 아닌 문자를 제거
- 소문자로 변환
- 앞과 뒤 공백을 제거

> 개별적으로 만든 slugify() 사용은 자제하는 것이 좋다. 비일관성으로 인해 나중에 데이터에 큰 문제가 발생 할 수 있다.

### 29.3.10 영어 이외에서의 slugification

- 영어 이외의 언어에서는 문제가 될 수 있다. 

```
>>> from django.utils.text import slugify
>>> slugify('straße') # 독일어
'strae'
```

- 다행히도 allow_unicode flag 를 이용하면 해결 할 수 있다.

```
>>> slugify('straße', allow_unicode=True) # Again with German
'straße'
```

### 29.3.11 django.utils.timezone

- Django의 timezone을 이용할 때 데이터베이스에는 UTC 포맷 형태로 저장하고 필요에 따라 지역 시간대에 맞게 변형하여 이용하자.

### 29.3.12 django.utils.translation

- django 의 다국어 지원 기능이다.

[다국어 지원 - WikiDocs](https://wikidocs.net/9824)


## 29.4 예외

### 29.4.1 django.core.exceptions.ImproperlyConfigured

- 설정 잘 못 되었을 때 발생
- Django 세팅 모듈을 import 할 때 세팅 모듈이 문제가 없는지 검사
예를 들어, settings.py의 값이 잘못되었거나 파싱 할 수없는 경우에 발생한다.

### 29.4.2 django.core.exception.ObjectDoesNotExist

- object가 없을 때 발생
- 이 예외를 이용하여 404 대신 403 예외를 발생시키는 자신만의 함수를 만들 수 있다.

```python
# core/utils.py
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied

def get_object_or_403(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        raise PermissionDenied
    except MultipleObjectsReturned:
        raise PermissionDenied
```

### 29.4.3 django.core.exception.PermissionDenied

- 인증된 사용자가 허가되지 않는 곳에 접소을 시도할 때 이용된다.
- 뷰에서 해당 예외를 발생시키면 뷰가 django.http.HttpResponseForbidden을 유발한다.
- 보안이 중요한 프로젝트 및 민감한 데이터를 조작하는 함수에서 유용하게 사용 될 수 있다.
예기치 않은 일이 발생했을 때 단순히 500 에러를 보여주는 것보다 'Permission Denied(접근 거부)'화면을 보여준다??ㅎㅎㅎㅎ

- PermissionDenied 예외가 403 에러 페이지를 표시하는 방법은 아래와 같다. root directory의 URLConf에 다음을 추가해준다.

```python
# urls.py

# 기본 view 는 django.views.defaults.permission_denied 다.
handler403 = 'core.views.permission_denied_view'
```

## 29.5 직렬화 도구와 역직렬화 도구

- REST API를 작성할 때를 위해 django 에서는 JSON, Python, YAML, XML 데이터를 위한 유용한 직렬화 도구와 역직렬화 도구를 제공한다.

- 아래는 직렬화 예제이다.
```python
# serializer_example.py
from django.core.serializers import get_serializer

from favorites.models import Favorite

# serializer 클래스 생성
# 'json'을 'python' 이나 'xml'로 바꾸어 이용해도 된다.
# pyyaml이 설치되어 있을 경우 'pyyaml'을 'json'대신 써도 된다.
JSONSerializer = get_serializer('json')
serializer = JSONSerializer()

favs = Favorite.objects.filter()[:5]

# 모델 데이터의 직렬화
serialized_data = serializer.serialize(favs)

# 다음 예제를 위해 직렬화된 데이터를 저장하기
with open('data.json', 'w') as f:
    f.write(serialized_data)
```

- 다음은 역직렬화 예제이다.
```python
# deserializer_example.py
from django.core.serializers import get_serializer

from favorites.models import Favorite
# serializer 클래스 생성
# 'json'을 'python' 이나 'xml'로 바꾸어 이용해도 된다.
# pyyaml이 설치되어 있을 경우 'pyyaml'을 'json'대신 써도 된다.
JSONSerializer = get_serializer('json')
serializer = JSONSerializer()

# 직렬화된 데이터 파일 열기
with open('data.txt') as f:
    serialized_data = f.read()
    
# 'python data'로 역직렬화된 모델 데이터 넣기
python_data = serializer.deserialize(serialized_data)

# python_data 처리
for element in python_data:
    # 'django.core.serializers.base.DeserializedObject' 출력
    print(type(element))
    
    # 인스턴스의 엘리먼트 출력
    print(
        element.object.pk,
        element.object.created
    )
```

- Django의 내장 직렬화 도구와 역직렬화 도구를 이용할 때는 언제든지 문제가 발생할 수 있다. 다음과 같은 가이드라인을 참고해라.
    - 간단한 데이터에 대해서만 직렬화를 한다.
    - 데이터베이스 스키마의 변화는 언제라도 직렬화된 데이터와 문제를 일으킬 수 있다.
    - 그냥 단순히 직렬화된 데이터를 임포트하지 말고, 언제나 장고 폼 라이브러리를 이용하여 데이터를 저장하기 전에 확인 작업을 거친다.

### 29.5.1 django.core.serializer.json.DjangoJSONEncoder

- Python 에 내장되어 있는 JSON 모듈 자체에는 날짜, 시간이나 소수점 데이터를 인코딩하는 기능이 빠져 있다.
- 그래서 Django 는 JSONEncoder 클래스라는 유용한 기능을 제공한다.
```python
# json_encoding_example.py
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

data = {'date': timezone.now()}

# DjangoJSONEncoder 클래스를 추가하지 않는다면 
# json library가 TypeError를 일이킬 것이다.
json_data = json.dumps(data, cls=DjangoJSONEncoder)

print(json_data)
```

### 29.5.2 django.core.serializers.pyyaml

- pyyaml 서드 파티 라이브러리로 구동된다.
- pyyaml이 지원하지 않는 Python-to-YAML으로 부터 시간 변환을 처리할 수 있다.
- 역직렬화는 yaml.safe_load() 함수를 이용한다.

### 29.5.3 django.core.serializers.xml_serializer

- 기본적으로 파이썬 내장 XML 핸들러를 이용한다.
- XML 폭탄 공격을 방지하기 위해 Christian Heimes의 `defusedxml` 라이브러리를 포함하고 있다.

### 29.5.4 rest_framework.serializers

- 장고의 내장 시리얼 라이저로는 충분하지 않을 때가 있습니다. 다음은 제한 사항에 대한 일반적인 예입니다.
    - 필드에 저장된 데이터 만 직렬화합니다. 메서드 나 속성의 데이터는 포함 할 수 없습니다.
    - 보안이나 성능을 위해 직렬화 된 필드는 변경 할 수 없습니다.

- 위와 같은 문제가 생기면 Django Rest Framework의 Serializers 도구 세트를 사용해라.
- 복잡하지만 처음부터 작성하는 것보다 좋다.
