# 14. 템플릿 태그와 필터

- 모든 기본 템플릿과 태그의 이름은 명확하고 직관적이어야 한다.
- 모든 기본 템플릿과 태그는 각각 한 가지 목적만을 수행한다.
- 기본 템플릿과 태그는 영속 데이텅 변형을 가하지 않는다.



## 14.1 필터는 함수다

- 필터는 장고 템플릿 안에서 파이썬을 이용할 수 있게 해 주는 데코레이터를 가진 함수이다.
- [실전예제: Custom template filter](https://anohk.github.io/2017-07-08/custom-template-filter/)
- [공식문서: custom template tags & filter](https://docs.djangoproject.com/ko/2.1/howto/custom-template-tags/)

### 14.1.1 필터들은 테스트하기 쉽다
- '22장 테스트, 정말 거추장스럽고 낭비일까?'에서 다루듯이 테스팅 함수를 제작하는 것으로 간단하게 할 수 있다.

### 14.1.2 필터와 코드의 재사용

- 대부분의 필터 로직은 다른 라이브러리로부터 상속되어 왔다.
- [소스코드: defaultfilter.py](https://github.com/django/django/blob/master/django/template/defaultfilters.py)
- django.template.defaultfilters.slugify 를 임포트할 필요 없이, django.utils.text.slugify 를 바로 임포트하여 사용
```python
# site-package/django/template/defaultfilters.py

from django.utils.text import slugify as _slugify

@register.filter(is_safe=True)
@stringfilter
def slugify(value):
    return _slugify(value)
```
```python
# site-package/django//utils/text.py

@keep_lazy(str, SafeText)
def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return mark_safe(re.sub(r'[-\s]+', '-', value))
```

- 필터들은 utils.py 모듈 같은 유틸리티 함수로 옮길수 있으며,
- 이렇게 함으로써 코드에 좀 더 집중할 수 있고 테스트를 쉽게 하고, 임포트문도 훨씬 적어진다.

### 14.1.3 언제 필터를 작성해야 하는가

- 필터는 데이터의 외형을 수정하는데 매우 유용
- REST API와 다른 출력 포맷에서 손쉽게 재사용 가능
- 두 개의 인자만 받을 수 있는 기능적 제약 때문에 필터를 복잡하게 이용하기가 매우 어려움(사실상 불가능)

## 14.2 커스텀 템플릿 태그

- 템플릿 태그와 필터에 너무 많은 로직을 넣을 경우 겪을 수 있는 문제들 살펴보기

### 14.2.1 템플릿 태그들은 디버깅하기 쉽지 않다

- 복잡한 템플릿 태그들은 디버깅하기 어려우며, 이 경우 로그와 테스트를 통해 도움을 받을 수 있다

### 14.2.2 템플릿 태그들은 재사용하기 쉽지 않다

- REST API, RSS 피드 또는 PDF/CSV 생성을 위한 출력 포맷 등을 동일 템플리 태그를 이용해 처리하기 쉽지않다
- 여러 종류의 포맷이 필요하다면 템플릿 태그 안의 로직을 utils.py 로 옮기는 것을 고려해보자

### 14.2.3 템플릿 태그의 성능 문제

- 템플릿 태그 안에서 또 다른 템플릿을 로드할 경우 심각한 성능 문제를 야기함
- 커스텀 템플릿 태그가 많은 템플릿을 로드한다면, 로드된 템플릿을 캐시하는 방법을 고려할 수 있다.
- [공식문서: template cached Loader](https://docs.djangoproject.com/en/1.11/ref/templates/api/#django.template.loaders.cached.Loader)

### 14.2.4 언제 템플릿 태그를 이용할 것인가

- 새로운 템플릿 태그를 추가하는 것에 대해 우리는 매우 조심스러운 입장이다.
- 새로운 템플릿을 추가하기 앞서 다음 사항을 고려하자
    - 데이터를 읽고 쓰는 작업을 할 것이라면 모델이나 Object method 가 더 좋다
    - 프로젝트 전반에서 일관된 작명법을 이용하고 있기 때문에 추상화 기반의 클래스 모델을 core.models 모듈에 추가할 수 있다.
     프로젝트의 추상화 기반 클래스 모델에서 어떤 메서드나 프로퍼티가 우리가 작성하려는 커스텀 템플릿 태그와 같은일을 하는가?
    - 그렇다면 언제 템프릿 태그를 작성할까? HTML을 렌더링하는 작업이 필요할 때

## 14.3 템플릿 태그 라이브러리 이름 짓기

- 템플릿 태그 라이브러리 작명의 관례는 {app_name}_tags.py 다
- 템플릿 태그 라이브러리 이름을 앱과 똑같이 짓지 말아라.
- 통합 개발 환경이나 텍스트 편집기에서 제공하는 템플릿 라이브러리 작명 기능에 의존하지 말아라.

## 14.4 템플릿 태그 모듈 로드하기

- 템플릿에서 `{% extends "base.html" %}` 바로 다음에 템플릿 태그가 로드될 수 있도록 하자
```
{% extends "base.html" %}

{% loads flavors_tags %}
```

### 14.4.1 반드시 피해야 할 안티 패턴 한 가지

```python
# 이 코드는 이용하지 말자! 악마 같은 안티 패턴이다!
# settings/base.py

TEMPLATES = [
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        # 이 코드는 이용하지 말자! 악마 같은 안티 패턴이다!
        'builtins': ['flavors.templatetags.flavors_tags'],
    },
]
```

- 문제점은 아래와 같다
    - 템플릿 태그 라이브러리를 django.template.Template에 의해 로드된 템플릿에 로드함으로써 오버헤드를 일으킨다
    이는 모든 상속된 템플릿, 템플릿 {% include %}, include_tag 등에 영향을 미친다
    - 템플릿 태그 라이브러리가 암시적으로 로드되기 때문에 디버깅이 쉽지 않다

## 14.5 요약

- **템플릿 태그와 필터들은 반드시 데이터를 표현하는 단계에서 데이터에 대한 수정**을 위해서만 쓰여야 한다.
