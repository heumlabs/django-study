# 11. 폼 패턴들

- 유용한 폼 관련 패키지
```
1) django-floppyforms: 장고 폼을 HTML5로 렌더링해 줌.
2) django-crispy-forms: 폼 레이아웃의 고급 기능들. 폼을 부트스트랩 폼 엘리머트와 스타일로 보여준다.
3) django-forms-bootstrap: 부트스트랩 스타일을 이용한 간단한 도구
```
- 아래와 같은 조합으로 사용을 추천함
```text
A) django-floppyforms + django-crispy-forms
B) django-floppyforms + django-forms-bootstrap
```


## 11.1 패턴1: 간단한 모델폼과 기본 유효성 검사기

- ModelForm은 기본적인 유효성 검사기를 제공한다.
```python
# flavor/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
    model = Flavor
    fields = ['title', 'slug', 'scoops_remaining']

class FlavorUpdateView(LoginRequiredMixin, UpdateView):
    model = Flavor
    fields = ['title', 'slug', 'scoops_remaining']
```
- 기본 유효성 검사기를 있는 그대로 이용하는 방법
    - Flavor 모델을 FlavorCreateView, FlavorUpdateView에서 이용하도록 한다.
    - 두 뷰에서 Flavor 모델에 기반을 둔 ModelForm을 자동 생성한다.
    - 생성된 ModelForm이 Flavor 모델의 기본 필드 유효성 검사기를 이용하게 된다.

## 11.2 패턴2: 모델폼에서 커스텀 폼 필드 유효성 검사기 이용하기

### 패턴2-1

- 예제 -> 모든 앱의 타이틀 필드가 'Tasty'로 시작되도록 하기 (문자열 유형성 검사)
- 방법 -> 커스텀 단일 필드 유효성 검사기를 생성하고, 추상화 모델과 폼에 추가하는 방법

- 1)유효성 검사를 위한 validators.py 작성
```python
# core/validators.py
from django.core.exceptions import ValidationError

def validate_tasty(value):
    """단어가 Tasty로 시작하지 않으면 ValidationError를 일으킨다."""
    if not value.startswith('Tasty'):
        msg = 'Must start with Tasty'
        raise ValidationError(msg)
```

- 2)프로젝트 전반에서 이용할 수 있는 추상화 모델 작성
```python
# core/models.py
from django.db import models
from .validators import validate_tasty

class TastyTitleAbstractModel(models.Model):
    title = models.CharField(max_length=255, validators=[validate_tasty])
    
    class Meta:
        abstract = True
```

- 3)Flovar 모델에 TastyTitleAbstractModel을 부모 클래스로 지정 (다른 모델에도 적용 가능함)
```python
# flavors/models.py
from django.db import models
from django.urls import reverse
from core.models import TastyTitleAbstractModel

class Flavor(TastyTitleAbstractModel):
    slug = models.SlugField()
    scoops_remaining = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('flavors:detail', kwargs={'slug': self.slug})
```

### 패턴2-2

- 예제 -> 폼에만 validate_tasty()를 이용하고자 할 때, 다른 필드에 적용하고 싶을 때
- 방법 -> 커스텀 FlavorForm을 작성하고 이를 뷰에 추가

- 1)FlavorForm 작성
```python
# flavors/forms.py
from django import forms
from .models import Flavor
from core.validators import validate_tasty

class FlavorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlavorForm, self).__init__(*args, **kwargs)
        self.fields['title'].validators.append(validate_tasty)
        self.fields['slug'].validators.append(validate_tasty)
        
    class Meta:
        model = Flavor
```

- 2)커스텀 폼을 뷰에 추가
    - 뷰의 모델 속성을 기반으로 모델폼을 자동으로 생성
    - 이렇게 기본 생성된 모델폼에 우리의 커스텀 FlavorForm 을 오버라이딩
```python
# flavors/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Flavor
from .forms import FlavorForm

class FlavorActionMixin:
    model = Flavor
    fields = ['title', 'slug', 'scoops_remaining']

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FlavorActionMixin, self).form_valid(form)

class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin, CreateView):
    success_msg = 'created'
    # FlavorForm 클래스를 명시적으로 추가
    form_class = FlavorForm

class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin, UpdateView):
    success_msg = 'updated'
    # FlavorForm 클래스를 명시적으로 추가
    form_class = FlavorForm

class FlavorDetailView(DetailView):
    model = Flavor
```

## 11.3 패턴3: 유효성 검사의 클린 상태 오버라이딩하기

- 아래와 같은 상황에서는 clean() 또는 clean_<field name>() 메서드를 오버라이딩 하는 것이 적합하다.
    - 다중 필드에 대한 유효성 검사
    - 이미 유효성 검사가 끝난 데이터베이스의 데이터가 포함된 유효성 검사

- Django는 기본 또는 커스텀 필드 유효성 검사기를 실행한 후, clean() 또는 clean_<field name>() 메서드를 이용하여 입력된 데이터의 유효성 검사를 다시 한다.
- 이유는 아래와 같다.
    - clean() 메서드는 두 개 또는 그 이상의 필드들에 대해 서로 간의 유효성을 검사하는 공간이 된다.
    - 클린(clean) 유효성 검사 상태는 영속 데이터(persistent data)에 대해 유효성을 검사하기에 좋다.

- 예제) 아이스크림을 선택할 때 재고가 없는 경우 (clean_slug() 메서드 사용)
```python
# flavors/forms.py
from django import forms
from flavors.models import Flavor

class IceCreamOrderForm(forms.Form):
    """일반적으로 forms.ModelForm을 이용하면 된다.
    하지만 모든 종류의 폼에서 이와 같은 방식을 적용할 수 있음을 보이기 위해 forms.Form을 이용했다.
    """
    slug = forms.ChoiceField(label='Flavor')
    toppings = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super(IceCreamOrderForm, self).__init__(*args,
        **kwargs)
    
        # 선택 가능한 옵션을 (모델의) flavor 필드에서 설정하지 않고 여기서 동적으로 설정했다.
        # 필드에서 설정하면 서버를 재시작하지 않고는 폼에 설정 상태를 변경할 수 없기 때문이다.
        self.fields['slug'].choices = [
            (x.slug, x.title) for x in Flavor.objects.all()
        ]
        # 주의: 필터를 이용하여 아이스크림이 남았는지 확인할 수도 있으나 filter()가 아닌 clean_slug를 이용하는 방법을 예로 들었다.
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Flavor.objects.get(slug=slug).scoops_remaining <= 0:
            msg = 'Sorry, we are out of that flavor.'
            raise forms.ValidationError(msg)
        return slug
```

- 예제) 두 개의 필드의 유효성을 검사하는 경우 (clean() 메서드 사용)
```python
# flavors/forms.py
# 앞의 예제에 추가
def clean(self):
    cleaned_data = super(IceCreamOrderForm, self).clean()
    slug = cleaned_data.get('slug', '')
    toppings = cleaned_data.get('toppings', '')

    # "too much chocolate" 유효성 검사 예
    in_slug = 'chocolate' in slug.lower()
    in_toppings = 'chocolate' in toppings.lower()
    if in_slug and in_toppings:
        msg = 'Your order has too much chocolate.'
        raise forms.ValidationError(msg)
    return cleaned_data
```

## 11.4 패턴4: 폼 필드 해킹하기(두 개의 CBV, 두 개의 폼, 한 개의 모델)

- 나중에 입력할 필드가 있는 모델
```python
# stores/models.py
from django.db import models
from django.urls import reverse

class IceCreamStore(models.Model):
    title = models.CharField(max_length=100)
    block_address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return reverse('store_detail', kwargs={'pk': self.pk})
```

- 실체화된 폼 객체는 유사 딕셔너리 객체인 fields 속성 안에 그 필드들을 저장한다.
- 따라서 ModelForm의 __init__()메서드에서 새로운 속성을 적용하면 된다.
```python
# stores/forms.py
from django import forms
from .models import IceCreamStore

class IceCreamStoreCreateForm(forms.ModelForm):
    class Meta:
        model = IceCreamStore
        fields = ['title', 'block_address', ]

class IceCreamStoreUpdateForm(IceCreamStoreCreateForm):
    def __init__(self, *args, **kwargs):
        super(IceCreamStoreUpdateForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['description'].required = True
        
    class Meta(IceCreamStoreCreateForm.Meta):
        # 모든 필드를 다 보여준다.
        fields = ['title', 'block_address', 'phone', 'description', ]
```
- 주의: Meta.fields를 이용하되 Meta.exclude는 절대 이용하지 마라(26장의 26.14 참고)

- 뷰의 적용 예시
```python
# stores/views
from django.views.generic import CreateView, UpdateView
from .forms import IceCreamStoreCreateForm, IceCreamStoreUpdateForm
from .models import IceCreamStore

class IceCreamCreateView(CreateView):
    model = IceCreamStore
    form_class = IceCreamStoreCreateForm

class IceCreamUpdateView(UpdateView):
    model = IceCreamStore
    form_class = IceCreamStoreUpdateForm
```

## 11.5 패턴5: 재사용 가능한 검색 믹스인 뷰

- 각각 두 개의 모델에 연동되는 두 개의 뷰에 하나의 폼을 재사용 하는 예제
- 두 모델 모두 title이라는 필드가 있다는 가정하에, 검색 믹스인 만들기
```python
# core/views.py
class TitleSearchMixin:
    def get_queryset(self):
        # 부모의 get_queryset으로부터 queryset을 가져오기
        queryset = super(TitleSearchMixin, self).get_queryset()
        # q 라는 GET 파라미터 가져오기
        q = self.request.GET.get('q')
        if q:
            # 필터된 쿼리셋 반환
            return queryset.filter(title__icontains=q)
        # q 가 지정되지 않으면 그냥 쿼리셋 반환
        return queryset
```

- 각각의 뷰에 적용하기
```python
# add to flavors/views.py
from django.views.generic import ListView
from .models import Flavor
from core.views import TitleSearchMixin

class FlavorListView(TitleSearchMixin, ListView):
    model = Flavor
```
```python
# add to stores/views.py
from django.views.generic import ListView
from .models import Store
from core.views import TitleSearchMixin

class IceCreamStoreListView(TitleSearchMixin, ListView):
    model = Store
```
