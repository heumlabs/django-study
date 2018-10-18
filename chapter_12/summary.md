# 12. Form 기초

모든 Django project는 Form을 써야한다.

## 12.1 Django 폼을 이용해 입력된 데이터 검증하기

- 나쁜 예제
    
    ```python
    import csv
    import StringIO
    
    from .models import Purchase
    
    def add_csv_purchases(rows):
    
      rows = StringIO.StringIO(rows)
      records_added = 0
      
      # 한 줄당 하나의 dict를 생성. 단 첫 번째 줄은 키값으로 함
      for row in csv.DictReader(rows, delimiter=","):
        # 절대 따라하지 말 것. 유효성 검사 없이 바로 모델로 데이터 입력.
        Purchase.objects.create(**row)
        records_added += 1
        return records_added
    ```
    - 셀러가 존재하는지 유효성 검사를 하지않는다.
    - 유효성 검사 코드를 추가할 수 있지만, 데이터가 바뀔 때 마다 복잡한 유효성 검사 코드를 유지보수 해야한다. 즉, 번거로워진다.

- Form을 이용한 예제

    ```python
    import csv
    import StringIO
    
    from django import forms
    
    from .models import Purchase, Seller
    
    class PurchaseForm(forms.ModelForm):
      
      class Meta:
        model = Purchase
      
      def clean_seller(self):
        seller = self.cleaned_data["seller"]
        try:
          Seller.objects.get(name=seller)
        except Seller.DoesNotExist:
          msg = "{0} does not exist in purchase #{1}.".format(
            seller,
            self.cleaned_data["purchase_number"]
          )
          raise forms.ValidationError(msg)
        return seller
      
      def add_csv_purchases(rows):
        
        rows = StringIO.StringIO(rows)
        
        records_added = 0
        errors = []
        # 한 줄당 하나의 dict 생성. 단 첫 번째 줄은 키 값으로 함
        for row in csv.DictReader(rows, delimiter=","):
          
          # PurchaseForm에 원본 데이터 추가.
          form = PurchaseForm(row)
          # 원본 데이터가 유효한지 검사.
          if form.is_valid():
            # 원본 데이터가 유효하므로 해당 레코드 저장.
            form.save()
            records_added += 1
          else:
            errors.append(form.errors)
        
        return records_added, errors     ```
    
> #### code 파라미터는 어떻게 할 것인가?
> 
> 아르노 랭부르는 Django 공식 문서에서, ValidationError에 code 파라미터를 전달해 줄 것을 추천했다.
> 
> ```python
> forms.ValidationError(_('Invalid value'), code='invalid')
> ```

## 12.2 HTML 폼에서 POST 메서드 이용하기

데이터를 변경하는 모든 HTML 폼은 POST 메서드를 이용하여 데이터를 전송하게 된다.

```
<form action="{% url "flavor_add" %}" method="POST">
```

폼에서 POST 메서드를 이용하지 않는 유일한 경우는 검색 폼이다. 검색 폼은 일반적으로 어떤 데이터도 변경하지 않기 때문이다. 검색 폼은 데이터 변경을 이용하지 않기 때문에 GET 메서드를 이용할 수 있다.

## 12.3 데이터를 변경하는 HTTP 폼은 언제나 CSRF 보안을 이용해야 한다.

장고에는 CSRF(cross-site request forgery protection, 사이트간 위조 요청 방지)가 내장되어 있다.

경험상, CSRF 보호가 사용되지 않을 때는 `django-rest-framework-jwt`와 같이 검증된 라이브러리에 의해 인증된 machine-accessible API를 만드는 경우다. 이런 툴은 Django REST Framework를 이용할 때 사용한다.  
API 요청은 요청별로 서명/인증되어야 하므로 인증을 위해 HTTP 쿠키에 의존하는 것은 현실적이지 않다. 따라서 이러한 프레임워크를 사용할 때 CSRF가 항상 문제가 되는 것은 아니다.

데이터를 직접 변경하는 API를 만든다면, 아래의 문서를 참고하도록 하자.

참고문서: [[CSRF]](docs.djangoproject.com/en/1.11/ref/csrf/)

`csrf_protection`을 수동으로 뷰에 적용시키는 것 보다, `CsrfViewMiddleware`를 사용하도록 한다.

### 12.3.1 AJAX를 통해 데이터 추가하기

AJAX를 통해 데이터를 추가할 때는 반드시 Django의 CSRF 보안을 이용해야 한다. 절대 AJAX 뷰를 CSRF에 예외 처리하지 말기 바란다.  
대신 AJAX를 통해 데이터를 보낼 때 HTTP 헤더에 X-CSRFToken을 설정해 두도록 한다.

참고문서: [[CSRF AJAX]](https://docs.djangoproject.com/en/1.11/ref/csrf/#ajax)

챕터 17.6 AJAX와 CSRF 토큰에서 자세히 알아본다.

## 12.4 Django의 Form 인스턴스 속성을 추가하는 방법 이해하기

Django Form의 `clean()`, `clean_FOO()`, `save()` 메서드에 추가로 폼 인스턴스 속성이 필요한 때가 있다.

- Form 예시

    ```python
    from django import forms
    
    from .models import Taster
    
    class TasterForm(forms.ModelForm):
      
      class Meta:
        model = Taster
      
      def __init__(self, *args, **kwargs):
        # 폼에 user attribute 추가
        self.user = kwargs.pop('user')
        super(TasterForm, self).__init__(*args, **kwargs)
    ```
    
    `super()` 호출 전, `self.user` 추가

- View 예시

    ```python
    from django.views.generic import UpdateView

    from braces.views import LoginRequiredMixin
    
    from .forms import TasterForm
    from .models import Taster
    
    class TasterUpdateView(LoginRequiredMixin, UpdateView):
      model = Taster
      form_class = TasterForm
      success_url = "/someplace/"
      
      def get_form_kwargs(self):
        """keyward arguments로 Form을 추가하는 메서드"""
        # 폼의 #kwargs 가져오기
        kwargs = super(TasterUpdateView, self).get_form_kwargs()
        # kwargs의 user_id 업데이트
        kwargs['user'] = self.request.user
        return kwargs
    ```
    
## 12.5 폼 유효성 검사하는 방법 알아두기

#### `form.is_valid()` 호출 시, 일어나는 일
1. `form.is_valid()`가 `form.full_clean()` 호출
2. `form.full_clean()`은 폼 필드들과 각각의 필드 유효성을 하나하나 검사한다.
    1. 필드에 들어온 데이터에 대해 `to_python()`을 이용하여 파이썬 형식으로 변환, 변환 실패시에  `ValidationError`를 일으킨다.
    2. validator를 포함한 각 필드들에 특별한 유효성을 검사, 문제가 있는 경우 `ValidationError`를 일으킨다.
    3. 폼에 `clean_<field>()` 메서드가 있으면 이를 실행한다.
3. `form.full_clean()`이 `form.clean()` 메서드를 실행한다.
4. `ModelForm` 인스턴스인 경우, `form.post_clean()`이 다음 작업을 한다.
    1. `form.is_valid()`가 `True`나 `False`로 설정되어 있는 것과 관계없이 `ModelForm`의 데이터를 모델 인스턴스로 설정한다.
    2. 모델의 `clean()` 메서드를 호출한다. 참고로 ORM을 통해 모델 인스턴스를 저장할 때는 모델의  clean() 메서드가 호출되지 않는다.

### 12.5.1 모델폼 데이터는 폼에 먼저 저장된 이후 모델 인스턴스에 저장된다.

ModelForm의 경우, 각기 다른 두 단계를 통해 저장된다.

1. 폼 데이터가 폼 인스턴스에 저장된다.
2. 폼 데이터가 모델 인스턴스에 저장된다.

```python
# core/models.py
from django.db import models

class ModelFormFailureHistory(models.Model):
  form_data = models.TextField()
  model_data = models.TextField()
```

```python
# flavors/views.py
import json

from django.contrib import messages
from django.core import serializers
from core.models import ModelFormFailureHistory

class FlavorActionMixin(object):

  @property
  def success_msg(self):
    return NotImplemented
  
  def form_valid(self, form):
    messages.info(self.request, self.success_msg)
    return super(FlavorActionMixin, self).form_valid(form)
  
  def form_invalid(self, form):
    """실패 내역을 확인하기 위해 유효성 검사에 실패한 폼과 모델을 저장한다"""
    form_data = json.dumps(form.cleaned_data)
    
    model_data = serializers.serialize("json", [form.instance])[1:-1]
    
    ModelFormFailureHistory.objects.create(
      form_data=form_data,
      model_data=model_data
    )
    return super(FlavorActionMixin, self).form_invalid(form)
```

## 12.6 Form.add_error()를 이용하여 폼에 에러 추가하기

Form.add_error() 메서드를 사용하여 Form.claen()을 더 간소화할 수 있게 되었다.

```python
from django import forms

class IceCreamReviewForm(forms.Form):
  # tester 폼의 나머지 부분이 이곳에 위치
  ...

  def clean(self):
    cleaned_data = super(TasterForm, self).clean()
    flavor = cleaned_data.get("flavor")
    age = cleaned_data.get("age")
    
    if flavor == 'coffee' and age < 3:
      # 나중에 보여줄 에러들을 기록
      msg = u"Coffee Ice Cream is not for Babies."
      self.add_error('flavor', msg)
      self.add_error('age', msg)

    # 항상 처리된 데이터 전체를 반환한다
    return cleaned_data
```

### 12.6.1 사용하기 좋은 다른 폼 메서드

[[Form.errors.as_data]](https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form.errors.as_data)  
[[Form.errors.as_json]](https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form.errors.as_json)  
[[Form.non\_field_errors]](https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form.non_field_errors)


## 12.7 만들어진 위젯이 존재하지 않는 필드

`django.contrib.postgres` 의 두 필드 `ArrayField`, `HStoreField`는 존재하는 Django HTML 필드와 잘 맞지 않는다. 두 필드에 해당하는 위젯은 전혀 제공되지 않는다.

이러한 경우에도 Form을 사용해야한다. (챕터 12.1를 참조)


## 12.8 사용자 지정 위젯

Django 1.11의 가장 좋은 기능 중 하나는 Django 위젯의 HTML을 재정의하거나 사용자 지정 위젯을 만들 수 있는 것이다.

- 사용자 지정 위젯을 만들 때의 참고 사항
    - 단순하게 보여주는 것만 집중한다.
    - 어떤 위젯도 데이터를 변경해서는 안된다. 위젯은 보여주기 위한 것이다.
    - Django 패턴을 따르고 `widgets.py`이라고 불리는 모든 맞춤형 모듈을 넣는다.

### 12.8.1 Built-In 위젯 오버라이딩

이 기술은 Bootstrap, Zurb 및 기타 응답성이 뛰어난 Front-end Framework와 같은 도구를 통합하는 데 유용하다. 단점은 기본 템플릿을 재정의하면 모든 위젯에 이러한 변경 사항을 적용하게 된다.

```python
# settings.py

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
   INSTALLED_APPS = [
       ...
       'django.forms',
       ...
]
```

이렇게 세팅한 다음, templates 디렉토리에 디렉토리를 `django/forms/templates`로 생성하고 템플릿 재지정을 시작하면 된다.

[[Django Form source code]](https://github.com/django/django/tree/master/django/forms/templates/django/forms/widgets)

[[Overriding built in widget templates]](https://docs.djangoproject.com/en/1.11/ref/forms/renderers/#overriding-built-in-widget-templates)

[[template setting]](docs.djangoproject.com/en/1.11/ref/forms/renderers/#templatessetting)

### 12.8.2 새로운 사용자 지정 위젯

위젯을 보다 세부적으로 제어하여 특정 데이터 유형에 대한 변경 사항을 제한하려는 경우 사용자 지정 위젯을 생성하는 방법을 모색해야 한다.

1. `https://github.com/django/django/blob/master/django/forms/`에서원하는 것과 가장 유사한 위젯을 선택한다.
2. 위젯을 원하는 대로 확장, 변경사항은 최소로!

```python
# flavors/widgets.py
from django.forms.widgets import TextInput


classIceCreamFlavorInput(TextInput):
    """아이스크림 맛은 항상 'Ice Cream'으로 끝나야 한다."""
     
    def get_context(self, name, value, attrs):
        context = super(IceCreamInput, self).get_context(name, value, attrs)
        value = context['widget']['value']
        if not value.strip().lower().endswith('ice cream'):
            context['widget']['value'] = '{} Ice Cream'.format(value)
        return context
```

위 예시는 어리석지만 목적에 맞게 기존 위젯을 확장하는 방법을 보여준다.

- 위젯이 수행하는 모든 작업은 값이 표시되는 방식을 수정하는 것이다.
- 위젯은 브라우저에서 돌아오는 데이터를 검증하거나 수정하지 않는다. 검증과 수정하는 책임은 form과 model에게 있다.
- `django.forms.widgets.TextField`의 최소 최소값을 확장한다.

## 12.9 참고자료

[[forms expands]](http://pydanny.com/tag/forms.html)  
[[Widget for ArrayField]](http://bradmontgomery.net/blog/2015/04/25/nice-arrayfield-widgets-choices-and-chosenjs//)  
[[Rendering custom Django widget]](https://docs.djangoproject.com/en/1.11/ref/forms/renderers/)


## 12.10 요약

폼을 파고들때는 코드 명확성과 테스트에 초점을 맞춰라.  
양식은 Django 프로젝트의 주요 검증 도구 중 하나이며 공격 및 우발적인 데이터 손상에 대한 중요한 방어 수단이다.