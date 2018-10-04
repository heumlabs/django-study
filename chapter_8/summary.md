# 8. 함수 기반 뷰와 클래스 기반 

## 8.1 함수 기반 뷰와 클래스 기반 뷰를 각각 언제 이용할 것인가? 

- 뷰를 구현할 때마다 어떤 것이 적당한지 생각하자.
- 저자는 클래스 기반 뷰를 더 선호
- 그래서, 클래스 기반 뷰로 구현했을 경우 특별히 더 복잡해지는 경우나 커스텀 에러 뷰들에 대해서만 함수 기반 뷰를 이용
- 뷰 선택에 도움이 되는 순서도(한 눈에 들어 오지 않는다. 위의 항목만 생각하자.) ![flowchart](http://i.imgur.com/lAu1qcO.jpg)

## 8.2 URLConf로부터 뷰 로직 분리하기

- 뷰와 URL의 결합은 최대한의 유연성을 제공하기 위해 느슨하게 구성되어야 한다.
    - 뷰 모듈은 뷰 로직을 포함
    - URL 모듈은 URL 로직을 포함
- 나쁜 예제
```python
from django.conf.urls import url
from django.views.generic import DetailView

from tastings.models import Tasting

urlpatterns = [
    url(r"^(?P<pk>\d+)/$",
      DetailView.as_view(
        model=Tasting,
        template_name="tastings/detail.html"),
      name="detail"),
    url(r"^(?P<pk>\d+)/result$",
      DetailView.as_view(
        model=Tasting,
        template_name="tastings/result.html"),
      name="result")
]
```
- **느슨한 결합**(loose coupling) 대신 단단하게 종속적인 결합(tight coupling)되어 재사용이 어렵다.
- **반복되는 작업을 하지 말라**는 철학에 위배
- URL들의 무한한 확장성이 파괴되어 클래스 상속이 불가능

### 8.3 URLConf에서 느슨한 결합 유지하기
- 반복되는 작업하지 않기: 뷰들 사이에서 인자나 속성이 중복 사용되지 않음
- 느슨한 결합: 하나 이상의 URLConf에서 뷰들이 호출 될 수 있음
- URLConf는 한 번에 한 가지씩 업무를 처리해야함
- 클래스 기반 뷰의 장점 활용: 상속 가능
- 무한한 유연성

### 8.3.1 클래스 기반 뷰를 사용하지 않는다면?
- 함수 기반 뷰를 사용해도 URLConf로 부터 뷰 로직을 분리하자

## 8.4 URL 이름공간(namespace) 이용하기
- URL 이름공간은 앱 레벨 또는 인스턴스 레벨에서의 구분자(:)를 제공
- tasting_detail 대신 tasting:detail 을 사용
- urls.py
```python
# 프로젝트 루트에 있는 urls.py
 urlpatterns+= [
   url(r'^tastings/', include('tastings.urls', namespace='tastings')),
 ]
```
- tastings/urls.py
```python
# tastings/urls.py
from django.conf.urls import url
from . import views
urlpatterns = [
	url(
		regex = r"^$",
		view=views.TasteListView.as_view(),
		name="list"
	),
	url(
		regex = r"^(?P<pk>\d+)/$",
		view=views.TasteDetailView.as_view(),
		name="detail"
	),
	url(
		regex = r"^(?P<pk>\d+)/result/$",
		view=views.TasteResultsView.as_view(),
		name="result"
	),
	url(
		regex = r"^(?P<pk>\d+)/update/$",
		view=views.TasteUpdateView.as_view(),
		name="update"
	)
]
```
- tastings/views.py
```python
# tastings/views.py 코드조각
class TasteUpdateView(UpdateView):
	model = Tasting

	def get_success_url(self):
		return reverse("tastings:detail",
			kwargs={"pk":self.object.pk})	
```

### 8.4.1 URL 이름을 짧고 명확하고, 반복되는 작업을 피해서 작성하는 방법
- 모델의 이름이나 앱의 이름을 복사한 URL 대신 좀 더 (~~명확한~~)단순한 이름사용
- 시간이 절약되는 효과도 있음

### 8.4.2 서트 파티 라이브러리와 상호 운영성을 높이기
- <app_name>_detail 등의 이름으로 호출할 때 <app_name> 부분이 동일한 문제를 해결가능
- 서드 파티 라이브러리의 contact앱이 존재하며, 두번째 contact 앱을 추가해야할 경우
```python
# 프로젝트 루트에 있는 urls.py
urlpatterns += [
  url(r'^contact/', include('contactmoger.urls', namespace='contactmoger')),
  url(r'^report-problem/',include('contactapp.urls', namespace='contactapp')),
]
```
- 템플릿에서의 이용
```html
<a href="{% url "contactmoger:creaate" %}">Contact Us</a>
<a href="{% url "contactapp:report" %}">Report a Problem</a>
```

### 8.4.3 검색, 업그레이드, 리팩터링을 쉽게 하기
- tastings_detail 같은 코드나 이름은 용도가 애매모호하다: 뷰 이름인지, URL 이름인지, 또는 다른 어떤 것인지 헷갈림
- 대신 tastings:detail 이라고 쓰면 검색 결과가 명확하다

### 8.4.4 더 많은 앱과 템플릿 리버스 트릭을 허용하기
- 대부분의 꼼수(trick)은 프로젝트의 복잡성을 높인다.
- 참고할 만한 꼼수
    - 디버그 레벨에서 내부적인 검사를 실행하는 개발도구(django-debug-toolbar)
    - 최종 사용자에게 ‘모듈‘을 추가하게 하여 사용자 계정의 기능을 변경하는 프로젝트(??)

### 8.5 뷰에서 비즈니스 로직 분리하기
- 모델 메서드, 매니저 메서드, 유틸리티 헬퍼 함수들을 이용하여 비즈니스 로직을 구현하자
- 뷰에서 표준적으로 이용되는 구조 이외에 덧붙여진 비즈니스 로직은 뷰 밖으로 이동시키자


### 8.6 장고의 뷰와 함수
- 기본적으로 장고의 뷰는 HTTP를 요청하는 객체를 받아서 HTTP를 응답하는 객체로 변경하는 함수다.
- 수학에서 이야기 하는 함수와 개념상 매우 비슷
```python
# 함수로서의 장고 함수 기반 뷰
HttpResponse = view(HttpRequest)

# 수학에서 이용한 함수 식
y = f(x)

# 클래스 기반 뷰
HttpResponse = View.as_view()(HttpRequest)
```
- 클래스 기반 뷰의 경우 실제로 함수로 호출된다.
    - URLConf에서 View.as_view()라는 클래스 메서드는 실제로 호출이 가능한 뷰 인스턴스를 반환
    - 요청/응답 과정을 처리하는 콜백 함수 자체가 함수 기반 뷰와 동일하게 작동
    - [as_view() 메서드](http://ruaa.me/django-view/)

## 8.6.1 뷰의 기본 형태들
```python
# simplest_views.py
from django.http import HttpResponse
from django.views.generic import View

# 함수 기반 뷰의 기본 형태
def simplest_view(request):
  # 비즈니스 로직이 여기에 위치한다.
  return HttpResponse('FBV')

# 클래스 기반 뷰의 기본 형태
class SimplestView(View):
  def get(self, request, *args, **kwargs):
    # 비즈니스 로직이 여기에 위치한다.
   return HttpResponse('CBV')
```
- 한 기능만 따로 떼어 놓은 관점이 필요할 때가 있다
- (가장 단순한)기본 장고 뷰를 이해했다는 것은 장고 뷰의 역활을 명확하게 이해했다는 것
- 함수 기반 뷰는 HTTP 메서드에 중립적이지만, 클래스 기반 뷰의 경우 HTTP 메서드의 선언이 필요

## 8.7 locals()를 뷰 콘텍스트에 이용하지 말자
- [What is locals()](https://charsyam.wordpress.com/2018/05/03/%EC%9E%85-%EA%B0%9C%EB%B0%9C-%EC%8B%A0%EB%AC%98%ED%95%9C-python-locals-%EC%9D%98-%EC%84%B8%EA%B3%84/)
- locals()를 사용하는 것은 안티패턴이다.
- 명시적이었던 디자인이 암시적 형태로 변하여 뷰를 유지보수하기에 복잡한 형태로 만든다.
- 나쁜 예제
```python
# 위의 함수와 아래 함수의 차이점을 찾는데 얼마나 걸리는가?
def ice_cream_store_display(request, store_id):
  store = get_object_or_404(Store, id=store_id)
  date = timezone.now()
  return render(request, 'melted_ice_cream_report.html', locals())

def ice_cream_store_display(request, store_id):
  store = get_object_or_404(Store, id=store_id)
  now = timezone.now()
  return render(request, 'melted_ice_cream_report.html', locals())
```
- **명시적인 컨텐츠를 이용한 뷰**
```python
def ice_cream_store_display(request, store_id):
  return render(request, 'melted_ice_cream_report.html', dict{
    'store' : get_object_or_404(Store, id=store_id),
    'now' : timezone.now()
  })
```

## 8.8 요약
- 함수 기반 뷰와 클래스 기반 뷰 이용하는 경우 확인
- URLConf에서 뷰 로직은 분리하자
- 클래스 기반 뷰를 이용할 때 객체 상속이 가능하므로 코드를 재사용하기 쉬워지고 설계를 좀 더 유연하게 할 수 있다