# 13. Templates: Best Practices

- Django의 초기 디자인 결정 중 하나는 템플릿 언어의 기능을 제한하는 것
- Business Logic은 Python 쪽으로

## 13.1 대부분의 Template은 `templates/` 폴더에 두자

- 메인 `template/` 디렉토리에 보관. `template/`의 하위 디렉토리는 각 Django App에 해당.

```bash
# GOOD (메인 template 폴더에서 관리)
templates/
├── base.html
├── ... (other sitewide templates in here)
├── freezers/
│   ├── ("freezers" app templates in here)

# BAD (각 App 폴더 하위에서 관리)
freezers/
├── templates/
│   ├── freezers/
│   │   ├── ... ("freezers" app templates in here)
templates/
├── base.html
├── ... (other sitewide templates in here)
```

- 예외 : 플러그인 패키지로 설치된 Django App. 메인 'templates/'의 템플릿에서 오버라이딩하여 사용.

## 13.2 템플릿 구조 패턴

### 13.2.1 2중 템플릿 구조

- 모든 템플릿은 하나의 루트 파일 (base.html)에서 상속받음

```
templates/
├── base.html
├── dashboard.html # extends base.html
├── profiles/
│   ├── profile_detail.html # extends base.html
│   ├── profile_form.html # extends base.html
```

### 13.2.2 3-Tier Template Architecture Example

- 각각의 앱이 고유한 레이아웃을 가져야할 때
- 각 앱은 `base_<app_name>.html` 라는 앱 레벨 베이스 템플릿을 따로 가지고, 이들은 메인 템플릿인 `base.html`를 공유
- 각 앱 폴더 하위의 템플릿은 `base_<app_name>.html`을 상속받음
- `base.html`과 같은 레벨에 있는 템플릿은 `base.html`을 상속받음

```
templates/
├── base.html
├── dashboard.html # extends base.html
├── profiles/
│   ├── base_profiles.html # extends base.html
│   ├── profile_detail.html # extends base_profiles.html
│   ├── profile_form.html # extends base_profiles.html
```

### 13.2.3 Flat Is Better Than Nested

- 템플릿 블록을 가능한 한 단순한 상속 구조로 가져가서 유지보수가 쉽도록 한다.
- `python -c 'import this'`

## 13.3 템플릿에서 프로세싱 제한하기

- 템플릿에서 처리하는 양이 적을 수록 좋음
  - 특히, 템플릿에서 수행되는 쿼리와 반복 구문이 문제가 됨
  - 템플릿으로 쿼리셋을 보낼 때마다 쿼리셋의 크기, 검색되는 개체의 크기, 이 모든 필드가 다 필요한지, 루프 반복시 얼마나 많은 처리가 이루어지는지 생각해볼 것
- 캐시로 해결할 수 있지만 근본 원인을 고치자!

### 13.3.1 Gotcha 1: Aggregation in Templates

- 템플릿은 "이미 처리된" 데이터를 "보여주는" 용도로 사용. 합계 계산 등의 처리는 View에서.

### 13.3.2 Gotcha 2: Filtering With Conditionals in Templates

- 템플릿에서 많은 양의 Loop을 돌리면서 if문으로 필터링하지 않는다.
- 데이터베이스 계층에서 작업 수행

```
# BAD
{% for voucher in voucher_list %}
  {# Don't do this: conditional filtering in templates #} 
  {% if 'greenfeld' in voucher.name.lower %}
    <li>{{ voucher.name }}</li> {% endif %}
{% endfor %}
```

### 13.3.3 Gotcha 3: Complex Implied Queries in Templates

- `select_related` 사용

```
{% for user in user_list %}
  <li>
    {{ user.name }}:
    {# DON'T DO THIS: Generated implicit query per user #} {{ user.flavor.title }}
    {# DON'T DO THIS: Second implicit query per user!!! #} {{ user.flavor.scoops_remaining }}
  </li>
{% endfor %}
```

### 13.3.4 Gotcha 4: Hidden CPU Load in Templates

- 간단하게 보이는 템플릿 코드라도 많은 프로세싱이 필요할 수 있음
  - 이미지 처리 등
  - 뷰, 모델, helper methods, 혹은 Celery나 Django Channels과 같은 비동기 메시지 큐 사용

### 13.3.5 Gotcha 5: Hidden REST API Calls in Templates

- 위와 마찬가지
  - 예) 지도 API와 같은 외부 서비스 사용

## 13.4 Don’t Bother Making Your Generated HTML Pretty

- 읽기 쉬운 코드 (한 줄에 한 작업)
- 자동으로 압축 및 Minification을 도와주는 도구 사용 (24장 참고)

## 13.5 Exploring Template Inheritance

- `base.html` 아래의 block들로 같이 구성됨
  - `title`
  - `stylesheets`
  - `content`

- 예시 `about.html`
```
{% extends "base.html" %}
{% load staticfiles %}
{% block title %}About Audrey and Daniel{% endblock title %} {% block stylesheets %}
       {{ block.super }}
       <link rel="stylesheet" type="text/css"
href="{% static 'css/about.css' %}"> {% endblock stylesheets %}
{% block content %}
{{ block.super }}
<h2>About Audrey and Daniel</h2> <p>They enjoy eating ice cream</p>
{% endblock content %}
```

- 템플릿 태그
  - {% load %}: built-in 템플릿 태그 라이브러리 로딩
  - {% block %}: 부모 템플릿(`base.html`) 블럭 이용
  - {% static %}: Static Media
  - {% extend %}: `about.html`템플릿은 `base.html`을 상속/확장한 템플릿.

## 13.6 block.super Gives the Power of Control

- `{{ block.super}}`을 사용하면 부모 템플릿의 블럭 내용을 그대로 불러와서, 자식 템플릿에서 내용을 추가만 하면 됨
- `super()`와 비슷하지만 같지는 않음 : 인자를 받아들이지는 않음

## 13.7 Useful Things to Consider

### 13.7.1 Avoid Coupling Styles Too Tightly to Python Code

- 모든 템플릿의 스타일링은 JS와 CSS로 컨트롤하는 것을 목표로 함

### 13.7.2 Common Conventions

- 컨벤션을 지키자
- 예시
  - 템플릿 이름 : 대시(-)보다 밑줄(_)
  - 블럭 이름 : 명확하게 (`{% block javascript %}`)
  - 블럭 끝에도 블럭 이름 : `{% endblock javascript %}`

### 13.7.3 Use Implicit and Named Explicit Context Objects Properly

- 암묵적 Object와 명시적 Object를 적절히 사용
  - 명시적
    - {{object}}, {{object_list}} 대신에 명시적인 {topping_list}}, {{toppin}}을 이용할 수 있다
  - 암묵적 : 코드 재사용에 유리

### 13.7.4 Use URL Names Instead of Hardcoded Paths

- X : `<a href="/flavors/">`
- O : `<a href="{% url 'flavors:list' %}">`

### 13.7.5 Debugging Complex Templates

- settings의 TEMPLATES > OPTIONS : string_if_invalid 옵션 설정

```python
# settings/local.py
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS':
      'string_if_invalid': 'INVALID EXPRESSION: %s'
  },
]
```

## 13.8 Error Page Templates

- 적어도 404.html, 500.html 템플릿은 준비
- static file server에 준비
- 에러 페이지가 깨지는 일이 없도록 조심하자
- 예시
  - https://github.com/404


## 13.9 Follow a Minimalist Approach

- 템플릿 보다는 Python 쪽에 비즈니스 로직을!
- 템플릿에 로직이 있으면 재사용이 힘들다!
