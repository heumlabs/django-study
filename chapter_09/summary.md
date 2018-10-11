# 9. 함수 기반 뷰 Best practice

## 9.1 함수 기반 뷰의 장점

- 함수 기반 뷰 작성 가이드라인
    - 뷰 코드는 작을수록 좋다.
    - 뷰 코드 반복 사용은 지양한다.
    - 뷰에서는 프레젠테이션 로직을 처리해야한다. 비즈니스 로직은 모델 또는 폼에 내재시키자.
    - 뷰는 단순하게 유지하자.
    - 403, 404, 500을 처리하는 커스텀 코드를 쓰는 데 이용하자.
    - 복잡하게 중첩된 if 구문을 피하자.

## 9.2 HttpRequest 객체 전달하기

- 뷰에서 코드 재사용을 원하는 경우, 미들웨어(middleware)나 컨텍스트 프로세서(context processors) 같은 글로벌 액션에 연동되어 있지 않은 경우 문제가 발생한다. 따라서 재사용을 원하는 코드는 유틸리티 함수로 만드는 것을 추천한다.
- 많은 유틸리티 펑션들은 `djagno.http.HttpRequest` 객체의 속성을 가져와서 이용한다. 이 요청 객체는 함수나 메서드의 인자를 관리하는데 있어서 적은 부하를 가져다 준다.
- HttpRequest 객체를 이용하면, 클래스 기반 뷰로 통합하기가 쉬워진다.

## 9.3 편리한 데코레이터

함수가 주는 단순 명료함 + 데코레이터의 간편 표기법 = 언제 어디서나 사용이 가능하며 재사용이 가능한 매우 유용하고 강력한 도구 (ex. `django.contrib.auth.decorators.login_required`)

> ##### 간편 표기법이란?
> 
> 표현이나 가독성을 좋게 하기위해 프로그래밍 언어에 추가된 문법

### 9.3.1 데코레이터 남용하지 않기

- 너무 많은 데코레이터의 집합은 데코레이터 자체를 난해하게 만들어, 복잡한 상속 과정을 지닌 뷰가 오히려 단순해 보일 정도가 될 수 있다.
- 데코레이터를 이용할 때는 뷰에 사용될 데코레이터의 개수를 제한하는 것이 좋다.

### 9.3.2 데코레이터에 대한 좀 더 많은 자료들

- [데코레이터와 펑셔널 파이썬](http://www.brianholdefehr.com/decorators-and-functional-python)
    - 함수란 특정 작업을 수행하는 코드 블럭이다.
    - 데코레이터란 다른 함수의 기능을 수정하는 함수이다.
- [데코레이터 요약](https://www.pydanny.com/python-decorator-cheatsheet.html)

## 9.4 HttpResponse 객체 넘겨주기

HttpRequest 객체와 마찬가지로, HttpResponse 객체도 함수와 함수사이에 서로 전달받을 수 있다. 

선택적으로 사용 할 수 있는 `Middleware.process_template_request()`를 예시로 들 수 있다.

위의 기능은 데코레이터와 같이 사용하여 큰 효과를 볼 수 있다.

[process_template_request](https://docs.djangoproject.com/en/1.11/topics/http/middleware/#process-template-response)


## 9.5 요약

- 모든 함수는 HttpRequest 객체를 받고, HttpResponse 객체를 반환한다.
- HttpRequest와 HttpResponse를 함수를 이용해 변경할 수 있으며, 데코레이터를 이용하는 것도 가능하다.

