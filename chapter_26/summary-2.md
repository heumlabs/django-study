## 26.13 사용자가 올린 파일 다루기

- 사용자가 제공한(올린) 콘텐츠는 서버에 저장하는 것보다 content delivery networks(CDNs)를 이용하자.

### 26.13.1  CDN을 이용할 수 없는 경우

- 서버로 업로드된 파일들은 실행이 불가능한 폴더에 저장하는 것이 좋다.
- 업로드가 가능한 파일 확장자 리스트 관리
- CGI나 PHP 스크립트를 업로드하고 URL을 통해 접근하고 해당 파일을 실행 시킬 수 있으니 웹 서버 설정에 주의를 기울여라.
    - [CGI (Commom Gateway Interface)](https://users.cs.cf.ac.uk/Dave.Marshall/PERL/node187.html)
        - CGI 스크립트는 웹 서버에서 실행되는 모든 프로그램을 의미한다.

### 26.13.2 Django와 사용자 업로드 파일

- 업로드되는 파일의 타입을 확인 할 수 있는 방법
    - [python-magic](https://github.com/ahupp/python-magic) 라이브러리를 이용하여 업로드된 파일의 헤더를 확인
    - 특정 파일 타입에만 작동하는 python 라이브러리 이용
        - PIL(Python Image Library) 이용하여 파일이 진짜 이미지인지 확인 가능
    - defusedxml을 이용하자 26.21 장에서 자세히 설명

- [Warning] Custom Validator로는 충분하지 않다.
    - Custom Validator는 이미 필드의 to_python() 메서드로 파이썬화된 후에 실행이 되는 것이 때문에 custom validator는 이미 늦다.

## 26.14 ModelForms.Meta.exclude 사용하지 않기

- ModelForms를 이용할 때는 Meta.exclude 대신 **Meta.fields**를 이용해라
- Meta.exclude 를 이용할 경우, `대량 매개 변수 입력 취약점(mass assignment vulnerability)`과 같은 보안 위협이 발생할 수 있다.
    - 매개변수(예: 필드)를 명시화 하지 않으면 의도하지 않은 변수(필드)에 값이 입력 될 수 있다.
    - https://en.wikipedia.org/wiki/Mass_assignment_vulnerability
- 또 다른 이유로 Meta.exclude 를 이용할 경우, 모델 변경 후 다시 Form의 내용을 수정하지 않으면 의도하지 않은 필드에 값이 입력 될 수 있다.

## 26.15 ModelForms.Meta.fields='__all__' 사용하지 않기

- 위에서 이야기 했듯이 `대량 매개 변수 입력 취약점`예 노출 될 수 있다.

## 26.16 SQL Injection 공격 피하기

- SQL 문을 직접 사용하여 데이터베이스에 접속을 할 수 있으므로 아래의 경우에는 좀 더 세심함 주의가 필요하다.
    - .raw() ORM 메서드
    - .extra() ORM 메서드
    - [database cursor](https://ko.wikipedia.org/wiki/%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4_%EC%BB%A4%EC%84%9C)에 직접 접근하는 경우

## 26.17 신용카드 정보는 절대 저장하지 말라.

- [PCI-DSS 보안 표준](https://www.pcisecuritystandards.org/)과 PCI 규약을 확인하지 않은 상태로는 절대 신용카드 정보를 저장하지 말라
    - [PCI 규정 준수 체크리스트](https://www.akamai.com/kr/ko/resources/pci-compliance-checklist.jsp)
- 관련 정보를 대신 보관하며 관리하는 서드 파티 서비스를 이용하자.
    - Stripe
    - Braintree
    - Adyen
    - Paypal

## 26.18 사이트 모니터링하기

- 모니터링 도구 설치하고, 웹 서버의 액세스 및 오류 로그를 정기적으로 확인해라.

## 26.19 의존성(Dependencies) 최신으로 유지하기

- 새로운 릴리스에 보안패치가 포함되어 있다면 업데이트를 하자.(서드 파티의 의존성도 같이)
- PyPI가 제공하는 최신 버전과 requirements 파일을 자동으로 검사하는 [pyup.io](https://pyup.io/)를 사용하는 것을 추천
    - 최신 버전 및 보안이슈에 대해 1주일에 한 번 이메일을 발송해준다고함.

## 26.20 Clickjacking 예방하기

- Clickjacking 이란, 숨겨진 프레임이나 아이프레임 등에 다른 사이트로 로드되는 버튼을 숨겨서 사용자가 의도하지 않은 사이트로 로드가 되도록 하는 것
    - http://haker.tistory.com/102
- [Django 에서 제공하는 Clickjacking 예방 방법](https://docs.djangoproject.com/en/1.11/ref/clickjacking/)
    - 최신 브라우저는 리소스가 프레임 또는 iframe이 로드 될 수 있는지 여부를 나타내는 X-Frame-Options HTTP 헤더를 사용한다.
    response에 `SAMEORIGIN` 값이있는 헤더가 포함되어 있으면 요청이 동일한 사이트에서 발생한 경우 브라우저는 프레임의 리소스만로드한다.
    헤더가 `DENY`로 설정된 경우 브라우저는 어떤 사이트가 요청을 했는지에 관계없이 프레임에서 리소스가 로드되지 않도록 차단
    - setting.미들웨어에 'django.middleware.clickjacking.XFrameOptionsMiddleware' 추가
    - setting 에 X_FRAME_OPTIONS = 'DENY' 설정 추가

## 26.21 defusedxml을 이용하여 XML 폭탄 막기

- xml 폭탄 이란??
    - [Billion Laughs attack](https://en.wikipedia.org/wiki/Billion_laughs_attack)
    - [xml 문서의 구성 요소](http://tcpschool.com/xml/xml_dtd_component)
    
- lxml 과 같은 라이브러리는 잘 알려진 xml 기반 공격에 취약하다. 그래서 Christian Heimes이 [defusedxml](https://pypi.org/project/defusedxml/) 을 만들었다.

## 26.22 이중 인증(Two-factor authentication) 살펴보기

- 패스워드를 입력한 후 모바일기기를 통해 인증번호를 다시 입력 받는 것을 말한다.
- 모바일기기나 네트워크 접속이 어려운 사용자에게는 좋은 방법은 아니다.

## 26.23 SecurityMiddleware

- Django에 내장된 django.middleware.security.SecurityMiddleware 를 사용하는 것을 추천

## 26.24 강력한 패스워드 이용하게 만들기

- 패스워드를 생성할 때는 숫자 뿐만 아니라, 문자, 기호 등을 섞어서 생성하도록 해야 한다.

## 26.25 사이트 보안 검사하기

- 사이트에 대한 자동화 된 검진을 제공하는 여러 가지 서비스가 있습니다.
보안 감사는 아니지만 프로덕션 배포에 보안 허점이 없는지 확인하는 무료 방법입니다.

- pyup.io의 안전 라이브러리 (github.com/pyupio/safety)는 설치된 보안 취약성을 확인합니다.
기본적으로 Python 취약점 데이터베이스 인 Safety DB를 사용하지만, --key 옵션을 사용하여 pyup.io의 Safety API를 사용하도록 업그레이드 할 수 있습니다.

- Django 사이트를 외부에서 보안 점검을 할 수 있는 방법
    - [Pony Checkup](https://www.ponycheckup.com/)
- 모질라에서 제공하는 서비스(django 사이트가 아니여도 이용가능)
    - https://observatory.mozilla.org/

## 26.26 취약점 보고 페이지 만들기

- 사용자들이 보안 취약점을 발견했을 때, 이러한 내용을 올릴 수 있는 게시판(?)을 만들자
- 해당 내용의 보안을 인지하여 수정하면 사이트에 그 사람의 이름(아이디)를 게시하자.

## 26.27 순차적으로 증가하는 Primary Keys는 절대 사용자에게 공개하지 말라.

- 우리의 볼륨을 외부에 노출하게 되는 것이다.
- XSS 공격의 타겟이 된다.

### 26.27.1 slug를 이용하자.

- Django에 널리 사용이 되지만 slug가 중복이 될 경우 문제가 발생 할 수 도 있다.

### 26.27.2 UUIDs

- UUIDFields를 사용할 수 도 있다.

## 26.28 보안 설정 부록 참고

- Appendix G: Security Settings Reference

## 26.29 보안 패키지 목록 참고

- Appendix A: Packages Mentioned In This Book 의 Security 섹션 참고
- 보안 패키지 리스트

## 26.30 보안 사항에 대해 늘 최신 정보를 유지하라

- https://groups.google.com/forum/#!forum/django-announce 를 구독해라.
- 트위터와 [해커뉴스](https://news.ycombinator.com/) 등 보안관련 블로그를 주기적으로 확인해라
- 책추천
    - https://www.amazon.com/The-Tangled-Web-Securing-Applications/dp/1593273886/?ie=UTF8&tag=cn-001-20
    - https://www.amazon.com/The-Web-Application-Hackers-Handbook/dp/1118026470/?ie=UTF8&tag=cn-001-20


