# 15. Django Templates와 Jinja2


## 15.1 문법적인 차이

Django template language(이하 DTL)와 Jinja2는 문법적으로 매우 비슷하다. 이는 Jinja2가 DTL에서 영감을 얻었기 때문이다.  
(문법적 차이의 예시는 p209의 `Table 15.1: DTL vs Jinja2 Syntax Differences` 참조)

## 15.2 변경해야 하나요?

Django를 사용할 때, DTL과 Jinja2 중 어느 하나를 선택해서 사용할 필요는 없다. settings.TEMPLATES를 통해 일부 템플릿 디렉토리는 DTL를, 또다른 일부는 Jinja2를 사용할 수 있다.

### 15.2.1 DTL의 장점

- Django docs에 쉽고 명확하게 문서화 되어있으며, 템플릿 코드 예제들이 DTL을 사용하고 있다.
- DTL+Django 조합이 Jinja2+Django 조합보다 훨씬 더 많이 시도되었고, 더 성숙하다.
- 대부분의 써드파티 패키지들은 DTL을 사용한다. 이를 Jinja2로 변환하는데 추가 작업이 필요하다.
- 많은 양의 DTL code들을 Jinja2로 바꾸려면 큰 작업이 필요하다.

### 15.2.2 Jinja2의 장점

- Django와 독립적으로 사용 가능하다.
- Python 문법과 비슷하여 이해하기 쉽다.
- Jinja2가 조금 더 명시적이다. (ex. 함수를 호출할 때 괄호 사용)
- Logic에 임의의 제약이 덜하다. DTL의 경우 filter에 1개의 인자만 사용할 수 있지만 Jinja2는 무한대로 사용 가능하다.
- 벤치마크와 (저자의)실험에 따르면 일반적으로 Jinja2가 더 빠르다. (Chapter. 24 참고)

### 15.2.3 승자는?

- 신규 사용자는 DTL을 사용하는 것이 좋다.
- 많은 양의 코드가 있는 프로젝트는 몇몇의 페이지를 제외하고는 DTL을 사용하기를 원할 것이다.
- 경험이 풍부한 Djangonaut들은 각각의 장점을 평가하여 스스로 결정해라.

## 15.3 Jinja2를 사용할 때 고려해야 할 것

### 15.3.1 CSRF와 Jinja2

Jinja2는 DTL와 다른 방식으로 Django의 CSRF 메커니즘에 접근한다. Jinja2에서는 CSRF를 포함시키기 위해서 아래와 같은 특별한 HTML이 필요하다.

```html
<div style="display:none">
       <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
</div>
```

### 15.3.2 Jinja2에서 템플릿 태그 사용하기

Jinja2에서는 Django 스타일의 템플릿 태그를 사용할 수 없다. 특정 템플릿 태그의 기능이 필요한 경우, 아래와 같은 방법을 사용한다.

- 기능을 함수로 변환한다.
- Jinja2 Extension을 작성한다. [[참고링크]](http://jinja.pocoo.org/docs/dev/extensions/#module-jinja2.ext)

### 15.3.3 Jinja2 템플릿에서 Django 스타일의 템플릿 필터 사용하기

기본적으로, Django filter는 단순한 함수이므로(Chapter 14.1 참고), 템플릿 필터가 포함된 사용자 정의 Jinja2 환경을 쉽게 지정할 수 있다.

```python
# core/jinja2.py
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import defaultfilters
from django.urls import reverse

from jinja2 import Environment

def environment(**options):
  env = Environment(**options)
  env.globals.update({
      'static': staticfiles_storage.url,
      'url': reverse,
      'dj': defaultfilters
  })
  return env
```

Jinja2 템플릿의 함수로 Django 템플릿 필터를 사용하는 예:

```html
<table><tbody>
{% for purchase in purchase_list %}
    <tr>
        <a href="{{ url('purchase:detail', pk=purchase.pk) }}">
            {{ purchase.title }}
        </a>
    </tr>
    <tr>{{ dj.date(purchase.created, 'SHORT_DATE_FORMAT') }}</tr>
    <tr>{{ dj.floatformat(purchase.amount, 2) }}</tr> {% endfor %}
</tbody></table>
```

전역적으로 사용하고 싶지 않다면 mixin을 생성해서 View의 속성으로 연결하여 사용할 수 있다.

```python
# core/mixins.py
from django.template import defaultfilters

class DjFilterMixin:
    dj = defaultfilters
```

```
<table><tbody>
{% for purchase in purchase_list %}
    <tr>
        <a href="{{ url('purchase:detail', pk=purchase.pk) }}">
            {{ purchase.title }}
        </a>
    </tr>
    <!-- Call the django.template.defaultfilters functions from the view -->
    <tr>{{ view.dj.date(purchase.created, 'SHORT_DATE_FORMAT') }}</tr>
    <tr>{{ view.dj.floatformat(purchase.amount, 2) }}</tr>
{% endfor %}
</tbody></table>
```

> ##### Jinja2에서는 context processor의 사용을 피하라
> Django 공식 문서에서, Django 템플릿에서는 함수에 인자를 넣어서 부를 수 없기 때문에 context processor가 유용하다고 설명되어있다. Jinja2는 이러한 제약이 없기 때문에, context processor처럼 사용할 함수를 템플릿에 사용할 수 있는 글로벌 변수에 넣는 것을 추천한다. [[참고링크]](https://docs.djangoproject.com/en/1.11/topics/templates/#django.template.backends.jinja2.Jinja2)

### 15.3.4 Jinja2 Environment는 정적인 것으로 간주되어야 한다.

Jinja2 Environment는 설정, 필터, 테스트, 전역변수 등을 공유하는 객체이다. 프로젝트의 첫 번째 템플릿이 로드되면, 이 클래스를 정적인 객체로 인스턴스화 한다.

```python # core/jinja2.py
from jinja2 import Environment

import random


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        # Runs only on the first template load! The three displays below
        #   will all present the same number.
        #   {{ random_once }} {{ random_once }} {{ random_once }}
        'random_once': random.randint(1, 5)
        # Can be called repeated as a function in templates. Each call
        #   returns a random number:
        # {{ random() }} {{ random() }} {{ random() }}
        'random': lambda: random.randint(1, 5),
    })
    return env
```

> Jinja2 Environment를 수정하는 것은 굉장히 위험한 일이다.  
> Jinja2 API 문서에서는 "첫 번째 템플릿이 로드된 후 Environment의 수정은 엄청난 효과와 정의되지 않은 동작을 초래할 것입니다."라고 말한다.  
> [[참조링크]](http://jinja.pocoo.org/docs/dev/api/#jinja2.Environment)

## 15.4 참고자료

[[Django docs on using Jinja2]](docs.djangoproject.com/en/1.11/topics/templates/#django.template.backends.jinja2.Jinja2)
[[Jinja]](http://jinja.pocoo.org)

## 15.5 요약

이 장에서는 DTL과 Jinja2의 유사점과 차이점을 다루었다.  
또한 프로젝트에서 Jinja2를 사용할 경우의 몇 가지 결과 및 해결 방법을 살펴보았다.
