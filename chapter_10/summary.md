# 클래스 기반 뷰의 Best Practices

> CBV = Class Based View

- Class Based View(이하 CBV)의 `as_view()` Method는 callable(내장함수)를 반환
  - `django.views.generic.View`에 구현되어 있음. 모든 CBV는 이 클래스를 상속받음.
  - 같이 `as_view()` 정의 찾아보기!
- Generic CBV(이하 GCBV) : 공통적으로 많이 사용되는 패턴을 구현해놓음
  - [django-braces](https://github.com/brack3t/django-braces): 추가적인 Mixin 제공

## 10.1 CBV를 이용할 때의 Guideline

- View 코드는 적을 수록 좋다.
- View 안에서 코드를 반복하지 않는다.
- Business Logic은 가능한한 Model이나 Form에서 관리한다. View에서는 보여지는(Presentation) Logic만 관리한다.
- View는 Simple해야 한다.
- Mixin은 Simple해야 한다.
- (!) [`ccbv.co.uk`](ccbv.co.uk)와 친해지자
  - 모든 CBV가 정리되어있음. 특히 해당 CBV가 상속한 모든 Class를 정리하여 Attribute와 Method를 한 페이지에 정리해놓음. GOOOOD.

## 10.2 CBV와 Mixin 사용하기

- Mixin을 상속하여 사용할 때는 Kenneth Love가 제안한 상속 규칙을 추천  
  Python의 Method Resolution Order을 따름 (왼쪽에서 오른쪽으로 처리)
  1. Django에서 제공하는 기본 View는 항상 제일 오른쪽에 위치한다.
  2. Mixin 기본 뷰의 왼쪽에 위치한다.
  3. Mixin은 Python의 기본 object 타입을 상속해야 한다.

- 아래 예시 참고  
    ```python
    from django.views.generic import TemplateView 

    class FreshFruitMixin:  # Rule 3 : Python 3부터는 Class가 기본적으로 Python 기본 object 타입을 상속한다. 명시하지 않아도 된다.
        def get_context_data(self, **kwargs):
            context = super(FreshFruitMixin, self).get_context_data(**kwargs)
            context["has_fresh_fruit"] = True
            return context

    class FruityFlavorView(FreshFruitMixin, TemplateView):  # Rule 1,2 : Django 기본 View인 TemplateView은 제일 오른쪽에. Mixin은 그 왼쪽에
        template_name = "fruity_flavor.html"
    ```

- 참고 Link
  - [Python MRO 관련](https://makina-corpus.com/blog/metier/2014/python-tutorial-understanding-python-mro-class-search-path)

## 10.3 어떤 Task에 어떤 Django GCBV를 사용해야할까?

- GCBV는 최대 8개의 superlass가 상속되기도 하는 복잡한 상속 체인임
- GCBV 종류와 그 목적을 정리한 Table
    | 이름 | 목적 |
    | --- | --- |
    | View | 어디에나 사용할 수 있는 Base View | 
    | RedirectView | User를 다른 URL로 Redirect할 때 | 
    | TemplateView | Django HTML 템플릿을 보여줄 때  | 
    | ListView | 객체 목록 | 
    | DetailView | 객체를 보여줄 때 | 
    | FormView | 폼 Submit | 
    | CreateView | 객체를 생성할 때 | 
    | UpdateView | 객체를 Update할 떄 | 
    | DeleteView | 객체를 삭제할 때 | 
    | Generic date views | 시간에 걸쳐 발생하는 객체들을 나열해 보여줄 때 | 
- Django CBV/GCBV 사용에 대한 세 가지 의견
  1. "Generic View의 모든 종류를 이용하자!"
  2. "`django.views.generic.View`만 이용하자!"
  3. "View를 정말 상속할 것이 아니면 무시하자"

## 10.4 Django CBV에 대한 일반적인 Tip

### 10.4.1 Authenticated User에게만 Django CBV/GCBV 접근 가능하게 하기

- `LoginRequiredMixin` 사용
- `LoginRequiredMixin`사용할 때 `dispatch()` Method 오버라이딩 유의사항
  - `super(FlavorDetailview, self).dispatch(request, *args, **kwargs)`를 가장 먼저 호출
  - `super()` 호츌 이전에 실행되는 코드는 인증되지 않은 채로 실행되기 때문

### 10.4.2 View에서 Custom Action 구현하기 (with Valid Form)

- `form_valid()` Method 로직 추가

### 10.4.3 View에서 Custom Action 구현하기 (with Invalid Form)

- `form_invalid()` Method에 로직 추가

### 10.4.4 View Object 이용하기

- CBV를 컨텐츠 렌더링에 이용한다면, View 객체를 다른 Method나 Property에서 호출해서 이용하는 방법도 있음
  - Template에서도 호출 가능
- 아래 예시 참고
  - View
    ```python
    from django.contrib.auth.mixins import LoginRequiredMixin
    from django.utils.functional import cached_property
    from django.views.generic import UpdateView, TemplateView
    from .models import Flavor
    from .tasks import update_user_who_favorited


    class FavoriteMixin:
        @cached_property
        def likes_and_favorites(self):
            """Returns a dictionary of likes and favorites""" likes = self.object.likes()
            favorites = self.object.favorites()
            return {
                "likes": likes,
                "favorites": favorites,
                "favorites_count": favorites.count(),
            }

    class FlavorUpdateView(LoginRequiredMixin, FavoriteMixin, UpdateView): 
        model = Flavor
        fields = ['title', 'slug', 'scoops_remaining']
        
        def form_valid(self, form): 
            update_user_who_favorited(
                instance=self.object,
                favorites=self.likes_and_favorites['favorites']
            )
            return super(FlavorUpdateView, self).form_valid(form)

    class FlavorDetailView(LoginRequiredMixin, FavoriteMixin, TemplateView):
        model = Flavor
    ```
  - Template
    ```
    {# flavors/base.html #}
    {% extends "base.html" %}
    {% block likes_and_favorites %} 
    <ul>
      <li>Likes: {{ view.likes_and_favorites.likes }}</li>
      <li>Favorites: {{ view.likes_and_favorites.favorites_count }}</li>
    </ul>
    {% endblock likes_and_favorites %}
    ```

## 10.5 GCBV와 Form 사용하기

## 10.6 그냥 django.views.generic.View 사용하기

- CBV의 HTTP Method에 직접 접근
- 아래 예시 참고 (`if request.method ==...`보다는 가독성이 좋음)
    ```python 
    from django.contrib.auth.mixins import LoginRequiredMixin 
    from django.http import HttpResponse
    from django.shortcuts import get_object_or_404
    from django.views.generic import View
    from .models import Flavor
    from .reports import make_flavor_pdf


    class FlavorPDFView(LoginRequiredMixin, View):
        def get(self, request, *args, **kwargs):
            # Handles display of the Flavor object
            flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
            return render(request, 
                "flavors/flavor_detail.html",
                {"flavor": flavor}
            )
        def post(self, request, *args, **kwargs):
            # Handles updates of the Flavor object
            flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
            form = FlavorForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect("flavors:detail", flavor.slug)
    ```
- non-HTML 컨텐츠(JSON, PDF 등)를 보여줄 때 (GET Method)
    ```python
    from django.contrib.auth.mixins import LoginRequiredMixin 
    from django.http import HttpResponse
    from django.shortcuts import get_object_or_404
    from django.views.generic import View
    from .models import Flavor
    from .reports import make_flavor_pdf


    class FlavorPDFView(LoginRequiredMixin, View):
        def get(self, request, *args, **kwargs):
        # Get the flavor
        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
        # create the response
        response = HttpResponse(content_type='application/pdf')
        # generate the PDF stream and attach to the response
        response = make_flavor_pdf(response, flavor)
        return response
    ```

## 10.7 추가 자료

- docs.djangoproject.com/en/1.11/topics/class-based-views/
- docs.djangoproject.com/en/1.11/topics/class-based-views/generic-display/
- docs.djangoproject.com/en/1.11/topics/class-based-views/generic-editing/
- docs.djangoproject.com/en/1.11/topics/class-based-views/mixins/
- docs.djangoproject.com/en/1.11/ref/class-based-views/
- (The GCBV inspector at) ccbv.co.uk
- python.org/download/releases/2.3/mro/
- pydanny.com/tag/class-based-views.html
- Useful CBV Libraries
  - [django-extra-views](https://github.com/AndrewIngram/django-extra-views)
  - [django-vanilla-views](https://github.com/tomchristie/django-vanilla-views/tree/master)
