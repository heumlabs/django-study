# CORS

## 개요

HTTP 요청은 기본적으로 Cross-Site HTTP Requests가 가능합니다.

`<img>` 태그로 다른 도메인의 이미지 파일을 가져오거나, `<link>` 태그로 다른 도메인의 CSS를 가져오거나, `<script>` 태그로 다른 도메인의 JavaScript 라이브러리를 가져오는 것이 모두 가능합니다.

하지만 <script></script>로 둘러싸여 있는 스크립트에서 생성된 Cross-Site HTTP Requests는 Same Origin Policy를 적용 받기 때문에 Cross-Site HTTP Requests가 불가능합니다. 즉, 프로토콜, 호스트명, 포트가 같아야만 요청이 가능합니다.

[[Same-Origin의 정의]](https://developer.mozilla.org/ko/docs/Web/Security/Same-origin_policy)

## CORS 요청 종류

Simple/Preflight, Credential/Non-Credential의 조합으로 4가지가 존재

### [Simple Request](https://developer.mozilla.org/ko/docs/Web/HTTP/Access_control_CORS#%EA%B0%84%EB%8B%A8%ED%95%9C_%EC%9A%94%EC%B2%AD)

- GET, HEAD, POST 중 한 가지 Method를 사용해야 함
- POST Method의 경우, Content-Type이 아래 중 하나여야 함
    - application/x-www-form-urlencoded
    - multipart/form-data
    - text/plain
- 커스텀헤더를 전송하지 말아야 함

Simple Request는 아래와 같이 처리됩니다.

1. 클라이언트가 서버에 요청
2. 서버가 클라이언트에게 회신하는 것으로 종료

### [Preflight Request](https://developer.mozilla.org/ko/docs/Web/HTTP/Access_control_CORS#%EC%82%AC%EC%A0%84_%EC%9A%94%EC%B2%AD)

Simple Request의 조건에 해당하지 않는 경우 브라우저는 Preflight Request 방식으로 처리합니다.  

- GET, HEAD, POST 이외의 다른 방식으로도 요청이 가능함
- application/xml처럼 다른 Content-Type으로 요청을 보낼 수 있음
- 커스텀 헤더를 사용할 수 있음

Preflight Request는 아래와 같이 처리됩니다.

1. 클라이언트가 서버에 예비 요청(Preflight Request)
2. 서버가 예비 요청에 대해 클라이언트에게 회신
3. 클라이언트가 서버에 본 요청(Actual Request)
4. 서버가 본 요청에 대해 클라이언트에게 회신하는 것으로 종료

### [Request with Credential](https://developer.mozilla.org/ko/docs/Web/HTTP/Access_control_CORS#%EC%9D%B8%EC%A6%9D%EC%9D%84_%EC%9D%B4%EC%9A%A9%ED%95%9C_%EC%9A%94%EC%B2%AD)

HTTP Cookie와 HTTP Authentication 정보를 인식할 수 있게 해주는 요청 방식

기본적으로, cross-site XMLHttpRequest 실행 내에서, 브라우저는 자격 증명을 위한 정보를 전송하지 않을 것입니다.
`withCredentials=true`를 이용해 쿠키를 요청에 포함시킬 수 있습니다.

```
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://example.com/', true);
xhr.withCredentials = true;
xhr.send(null);
```

### Request with Non-Credential


COSR 요청은 기본적으로 Non-Credential 요청으로, `withCredentials=true`를 지정하지 모든 요청이 해당 요청입니다.


## CORS 헤더

### [HTTP 응답 헤더](https://developer.mozilla.org/ko/docs/Web/HTTP/Access_control_CORS#HTTP_%EC%9D%91%EB%8B%B5_%ED%97%A4%EB%8D%94)

- Access-Control-Allow-Origin
    
    ```
    Access-Control-Allow-Origin: <origin> | *
    ```
    - origin 파라메터는 리소스에 접근하는 URI를 특정함
    - `*`를 사용하면, 어떤 호스트에서든 리소스에서 접근이 가능하게 됨

- Access-Control-Allow-Credentials
    
    ```
    Access-Control-Allow-Credentials: true | false
    ```
    - 리소스에 접근하는 경우 클라이언트 요청에 인증값이 담긴 쿠키를 보내야하는지의 여부
    

- Access-Control-Expose-Headers

    ```
    Access-Control-Expose-Headers: Content-Length
    ```
    - 기본적으로 브라우저에게 노출이 되지 않지만, 브라우저 측에서 접근할 수 있게 허용해주는 헤더를 지정

- Access-Control-Allow-Methods

    ```
    Access-Control-Allow-Methods: <method>[, <method>]*
    ```
    - 리소스에 접근하는 경우 허용된 메서드 혹은 메서드들을 지정
    - 사전 전달 요청에 대한 응답에 사용됨

- Access-Control-Allow-Headers

    ```
    Access-Control-Allow-Headers: <field-name>[, <field-name>]*
    ```
    - 리소스에 접근하는 경우 허용된 헤더 혹은 헤더들을 지정
    - 사전 전달 요청에 대한 응답에 사용됨

- Access-Control-Max-Age
    
    ```
    Access-Control-Max-Age: 86400
    ```
    - 사전 전달 요청에 대한 응답이 얼마나 캐시되어 있는지를 나타내는 초 단위의 값

### [HTTP 요청 헤더](https://developer.mozilla.org/ko/docs/Web/HTTP/Access_control_CORS#HTTP_%EC%9A%94%EC%B2%AD_%ED%97%A4%EB%8D%94)

- Origin

    ```
    Origin: <origin>
    ```
    - cross-site 접근 요청 혹은 사전 전달 요청의 출처를 가리킴

- Access-Control-Request-Method

    ```
    Access-Control-Request-Method
    ```
    - 실제 요청이 일어나는 경우 어떤 Method가 사용될 것인지 서버에 알려줌
    - 사전 전달 요청 시에 사용됨

- Access-Control-Request-Headers 

    ```
    Access-Control-Request-Headers: <field-name>[, <field-name>]*
    ```
    - 실제 요청이 일어나는 경우에 어떤 HTTP 헤더가 사용될 것인지 서버에 알려줌
    - 사전 전달 요청 시에 사용됨



### 참고

- [[XMLHttpRequest]](https://developer.mozilla.org/ko/docs/XMLHttpRequest)
