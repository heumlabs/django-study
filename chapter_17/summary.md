# 17. REST API 사용

## 17.1 클라이언트 디버깅하는 방법 배우기

클라이언트측 JavaScript를 디버깅하는 것은 console.log() 및 console.dir()문을 단순하게 작성하는 것 보다 훨씬 많다. 디버깅과 오류 찾기에는 많은 도구가 있다.

도구를 선택한 후에는 클라이언트 측 테스트 작성 방법을 익히는 것이 좋다.

[[Chrome DevTools]](https://developers.google.com/web/tools/chrome-devtools)  
[[Debugging Javascript]](https://developer.mozilla.org/en-US/docs/Mozilla/Debugging/Debugging_
JavaScript)

## 17.2 JavaScript로 구동되는 Static Asset Preprocessor 사용 고려

과거에는 JavaScript나 CSS 최소화(minification)를 포함한 모든 곳에서 Python을 사용해왔다.  
그러나 최근엔 JavaScript 커뮤니티가 Python 커뮤니티보다 이러한 툴들의 버전을 더 잘 유지하고 있다.  
JavaScript 커뮤니티에서 해당 부분을 자신들의 툴체인으로 해결함으로써 우리(Python 부분)는 이러한 다른 일에 집중할 수 있게 되었다.

참고자료  
[[JavaScript Minification]](https://youtu.be/7128a9SoV0M)

## 17.3 실시간 서비스가 왜 어려운가 (Latency 문제)

- 지구의 반대편에서 날아온 HTTP 요청을 주고받는 데 걸리는 시간은 눈에 띌 정도로 느리다.
- 로컬 네트워크에서도 네트워크 속도저하나 잠시 끊기는 문제(hiccups) 등이 발생할 수 있다.

> ##### Hiccups (in Programming)
>
> A hiccup might be due to a transient power level change, a program bug that is only encountered under very rare circumstances, or something else. Unlike hiccups in human beings, a hiccup in a computer or a network tends not to be followed by additional hiccups.

### 17.3.1 대책: Animation을 이용해 지연 시간 가리기

지연 시간 문제로부터 사용자의 주의를 분산시키는 JavaScript 기반의 애니메이션을 사용한다. 

### 17.3.2 대책: Transaction이 성공한 것 처럼 속이기

JavaScript framework에서 HTTP 요청을 처리하는 방법은 비동기식이라서 사용자에게 시각적으로 보여주려면 상당히 복잡한 절차를 거쳐야 한다.

### 17.3.3 대책: 지리적 위치에 기반을 둔 서버들

7개 대륙에 걸쳐 배치된 서버를 고려한다. 하지만 이 대책은 프로그래밍이나 데이터베이스 레벨의 문제가 아니다.

### 17.3.4 대책: 지역적으로 사용자 제한

때로는 선택의 여지가 없다. 지역적으로 사용자를 제한한다. 일부 지역의 사람들이 만족스럽지 않을 수 있지만, '해당 국가는 곧 지원될 예정입니다!'와 같은 문구를 통해 완화될 수 있다.

## 17.4 안티패턴 피하기

### 17.4.1 다중 페이지로 구성된 앱이 필요한 경우인데도 단일 페이지 앱으로만 구성하는 경우

예로 전통적인 CMS(Centers for Medicare & Medicaid Services) 사이트를 구축하는 경우를 생각해보자.

의사들의 목록을 검색하여 비교한다고 가정했을 때, 단일 페이지 앱에서는 쉽게 비교할 수 없다. 자세한 내용을 보려고 클릭을 하면 데이터가 슬라이딩 모달로 표시된다. 그리고 마우스 우클릭으로 탭을 여러 개를 열 수 없다. 새 탭을 열면 루트 검색 페이지로 이동된다. 개별 의사에 대한 정보를 인쇄하거나 메일로 보낼 수는 있겠지만, 여러개의 탭을 이용해서 비교하는 것에 비하면 끔찍하다.

### 17.4.2 기존 사이트를 업그레이드 하는 경우

새 버전의 사이트를 위해 기존의 사이트를 폐기하지 않는 경우에는, Front-end 전체를 한 번에 업그레이드하지 마라.

기존 프로젝트로 작업하는 경우 새 기능을 단일 페이지 앱으로 추가하는 것이 더 쉽다. 이를 통해 프로젝트 유지관리자는 기존 코드베이스의 안정성을 유지하면서 새로운 기능으로 향상된 경험을 제공할 수 있다.

### 17.4.3 테스트를 사용하지 않는 경우

해가 갈수록 클라이언트 사이드 작업 내용은 복잡해지고 난해해지고 있다. 22장에서 Django, Python 테스팅에 대한 내용을 다룬다. JavaScript 테스팅에 대한 참고자료는 아래 링크에 첨부

[[JavaScript unit test tools for TDD]](https://stackoverflow.com/questions/300855/javascript-unit-test-tools-for-tdd)

### 17.4.4 JavaScript 메모리 관리를 이해하지 않는 실수

단일 페이지 앱은 훌륭하지만, 사용자가 페이지를 오래 띄워 놓고 이용하는 복잡한 시스템의 경우, 브라우저상의 객체들이 긴 시간동안 존재하게 된다. 이러한 객체들이 잘 관리되지 않으면 브라우저가 느려지고 충돌이 일어나게 된다.

### 17.4.5 jQuery가 아닐 때 DOM에 데이터를 저장하는 것

수년간 jQuery를 이용하면서 우리중 몇몇 사람은 DOM 엘리먼트에 데이터를 저장했다. 하지만 다른 JS framework의 경우 해당 방식은 좋지 않다.

각각의 JS framework는 자체적으로 구현된 클라이언트 데이터를 처리하는 메커니즘을 가지고 있고, 그 방법을 따르지 않으면 해당 프레임워크가 지원하는 기능 중 일부를 잃을 위험이 있다.

## 17.5 AJAX와 CSRF 토큰

Django의 CSRF 보호는 AJAX를 사용할 때 불편함으로 다가온다. 하지만, CSRF 보호는 Django를 안전하게 만드는 기능 중 하나이므로, 비활성 금지!

##### CSRF 장애물을 극복하기 위한 방법

1. Back-end의 경우, POST, PATCH, DELETE 요청을 처리하는 API가 있을 때마다 항상 DRF를 사용하라.
2. Front-end의 경우, DRF의 내장된 [JS 클라이언트 라이브러리](https://www.django-rest-framework.org/topics/api-clients/#javascript-client-library)를 사용하여 Back-end와 연결하는 것을 추천한다.
3. 때로는 DRF 클라이언트 framework가 제공하는 것 이상으로 긴밀한 integration이 필요한 경우가 있다. 이러한 경우에는 CSRF 프레임워크에 의존하는 것이 중요하다.

참고자료  
[[DRF JS client library]](https://django-rest-framework.org/topics/api-clients/#javascript-client-library)  
[[Django CSRF docs]](https://docs.djangoproject.com/en/1.11/ref/csrf/)
[[DRF JWT]](https://github.com/GetBlimp/django-rest-framework-jwt)

> ##### CSRF 보호를 끄기 위한 구실로 AJAX를 사용하지 마라
>
> API가 JWT 인증만 허용하는 경우에는 CSRF 보호를 비활성화해도 된다. 쿠키 인증을 수락하면 잘못된 것이다.  
> 만약 django-rest-framwork-jwt를 사용하고 있지 않다면, CSRF를 비활성화 시킨 사이트를 구축하면 안된다.

### 17.5.1 적절한 settings.CSRF_COOKIE_HTTPONLY 설정

`CSRF_COOKIE_HTTPONLY` 토큰을 True로 설정하면 악의적인 JS가 CSRF 보호를 무시하기가 더 어려워진다. JS를 사용하여 쿠키에서 CSRF 토큰을 가져올 수 없게 된다.

jQuery를 기반으로 Django의 지침에 따라 숨겨진 CSRF 토큰을 페이지에서 가져오는 예시는 아래와 같다.

```html
<html>
<!-- Placed anywhere in the page, doesn't even need to
    be in a form as the input element is hidden -->
    {% csrf_token %}
</html>
```

```javascript
var csrfToken = $('[name=csrfmiddlewaretoken]').val();
var formData = {
     csrfmiddlewaretoken: csrfToken,
     name=name, age=age
    };
    $.ajax({
        url: '/api/do-something/'',
        data: formData,
        type: 'POST'
})
```

## 17.6 JavaScript 실력 높이기

### 17.6.1 기술 수준 확인

Rebbeca Murphey의 JS 실력 평가 도구를 참고

https://github.com/rmurphey/js-assessment

### 17.6.2 JavaScript 더 깊게 배우기

부록 C: 추가자료 참고

## 17.7 JavaScript 코딩 표준 따르기

JavaScript의 경우, Front-end 및 Back-end 작업에 대해 다음 가이드를 권장한다.

[[Felix Node.js Style Guide]](https://raw.githubusercontent.com/felixge/nodeguide.com/master/guide/style.pdc)  
[[Felix Node.js Style Guide 번역본]](https://pismute.github.io/nodeguide.com/style.html)  
[[Idiomatic.js]](https://github.com/rwaldron/idiomatic.js)

## 17.8 요약 
- 클라이언트 디버깅
- JavaScript tatic asset preprocessor
- 클라이언트측 안티패턴
- AJAX 및 CSRF 토큰
- JavaScript 기술 향상
- 유용한 자료들
