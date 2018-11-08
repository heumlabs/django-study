# CSRF

## 1. XSS 와 CSRF 비교

- XSS란?
    - Cross-site Scripting 으로 공격하려는 사이트에 스크립트를 넣어 공격하는 기법

- CSRF란?
    - 사이트간 요청 위조(Cross-Site request forgery)
    - 사용자가 자신의 의지와는 무관하게 공격자가 의도한 행위(수정, 삭제, 등록 등)를 특정 웹사이트에 요청하게하는 공격

- 차이점
    - XSS는 자바스크립트를 실행시키는 것이고, CSRF는 특정한 행동을 시키는 것

- 같은점
    - HTML 태그를 이용
    - CSRF는 XSS의 변종기법


## 2. XSS 샘플

- 시나리오
    - 특정 게시글을 읽으면 Client의 쿠키가 메시지창에 나오게 해보자.

- 예제
    1. 게시글을 작성한다. 제목은 많은 사람들의 어그로를 끌수 있게 자극적으로 작성한다.
    ![XSS-img-1](https://t1.daumcdn.net/cfile/tistory/23358B39575F9E8716)
    2. 내용에 script 문을 추가한다. script 문에는 쿠키의 정보가 포함된 alert 메시지를 뜨게하는 내용이 포함한다.
    ![XSS-img-2](https://t1.daumcdn.net/cfile/tistory/24355739575F9E8816)

- 방지책은?
    - 스크립트를 못쓰게 한다. (-> 현실적으로 불가능)
    - 특정 패턴을 만든다. (-> 악의적인 사이트를 못들어가게 한다)???
    - html의 태그를 지정된 태그 이외에는 모두 막는다.
    - **쿠키를 저장할 때 쿠키값을 랜덤으로 저장하게하거나 인증불가, 중요정보를 쿠키에 저장 못하게 한다. (가장 이상적인 방법)**


## 3. CSRF 샘플

- 시나리오
    - 관리자가 게시한 글을 공격자가 원하는대로 변경하기

- 예제
    1. 게시판에서 CSRF를 이용해 수정할 게시글(타겟)을 선정한다.
    ![CSRF-img-1](https://t1.daumcdn.net/cfile/tistory/2257CB44575FA44735)
    2. 게시글 수정 페이지의 소스를 확인한다.
    [게시판 글 수정 소스코드](sample1.html)
    3. 소스에서 원하는대로 데이터를 변경하기 위해 필요한 부분만 추려낸다.
    4. value에 변경할 데이터를 넣어준다.
    [변조를 위한 html 작성](sample2.html)
    5. 위 코드가 삽입된 게시글을 작성한다.
    ![CSRF-img-2](https://t1.daumcdn.net/cfile/tistory/235F9644575FA4472E)
    6. 해당 게시글을 읽게 되면 삽입된 코드가 실행되어 form태그의 내용이 post로 전송된다.
    ![CSRF-img-3](https://t1.daumcdn.net/cfile/tistory/2761FB44575FA4482C)
    ![CSRF-img-4](https://t1.daumcdn.net/cfile/tistory/260F0644575FA4490A)

- [예제 참고 사이트](http://rednooby.tistory.com/22)


## 4. Django에서의 CSRF 보안 

- form 태그를 가진 django template에 아래와 같이 csrf_input을 설정한다.

```html
<form action="" method="post">
{% csrf_input %}
<input name="username" id="username" type="text" />
<input name="password" id="password" type="password" />
```

- Client에서 해당 페이지를 요청할 때 아래와 같은 response를 받게 된다.

```html
<form action="" method="post">
<input type='hidden' name='csrfmiddlewaretoken' value='d7f6f683188d35958b0f453f6849a8d7' />
```

- csrfmiddlewaretoken 라는 이름의 hidden변수에 random 생성된 token값이 날라온다.

- 동시에 http header에도 동일한 token을 cookie로 저장한다.

```
Set-Cookie: csrftoken=d7f6f683188d35958b0f453f6849a8d7; expires=Mon, 10-Jul-2017 08:32:17 GMT; Max-Age=31449600; Path=/
```

- client에서 form 태그가 포함된 페이지에 데이터를 전송(request)할 때, cookie와 body에 동일한 token 인지 체크한다.

- Django에서 해당 token값이 없거나 잘못되었을 경우 403 에러를 발생한다.

- [참고 사이트](http://www.iorchard.net/2016/07/11/curl_django_csrf_token_transmit.html)


## 5. 적용방법

- 좀 더 다양한 적용 방법은 공식 사이트를 참고 [Cross Site Request Forgery protection](https://docs.djangoproject.com/en/2.1/ref/csrf/)