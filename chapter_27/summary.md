# 27. 로깅: 무엇에 쓰이는가?

## 27.1 어플리케이션 로그 vs 다른 로그

이 장에서는 어플리케이션 로그에 초점을 맞춘다. Python 웹 응용 프로그램에서 기록한 데이터를 포함하는 로그 파일은 응용 프로그램 로그로 간주된다.

어플리케이션 로그 외에도 서버 로그, 데이터베이스 로그, 네트워크 로그 등은 모두 운영 시스템에 대한 중요한 통찰력을 제공하므로 모두 똑같이 중요하다고 고려해야한다.

## 27.2 로깅이 있는 다른 이유

- 로깅은 스택 추적 및 기존 디버깅 도구가 충분하지 않은 상황에서 사용할 수 있는 툴이다.
- 서로 상호작용하거나 예측할 수 없는 상황이 가능성이 있는 경우, 로깅은 우리에게 무슨 일이 일어나고 있는지를 알 수 있는 통찰력을 준다.
- 사용자가 사용할 수 있는 로그 레벨은 `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`이 있다.

## 27.3 각 로그 레벨의 사용 시기

- Production 이외의 환경에서는 모든 레벨의 로그를 사용하는 것이 좋다.
- 로그 레벨은 프로젝트의 settings 모듈에서 제어된다.
- 부하 테스트 및 대규모 사용자 테스트를 고려해 권장사항을 조절하여 사용할 수 있다.
- Production 환경에서는 DEBUG를 제외한 모든 레벨의 로그를 사용하는 것이 좋다.
- 오류를 수정하기 위한 디버그 코드는 또다른 오류를 낳을 수 있다.

### 27.3.1 Log Catastrophes With CRITICAL

긴급한 주의가 필요한 곳에서만 CRITICAL 레벨을 사용하라.

- 이 로그 레벨은 코어 Django 코드에는 절대 사용되지 않지만, 매우 심각한 문제가 발생할 수 있는 모든 곳에서 사용해야한다.
- 예를 들어, 나의 코드가 내부의 웹 서비스에 의존하고 해당 웹 서비스가 핵심 기능의 일부인 경우에 그 서비스에 액세스 할 수 없는 경우에는 CRITICAL 레벨로 로깅해야한다.

### 27.3.2 Log Production error With ERROR

코드가 캐치하지 못하는 예외를 발생시킬 때 ERROR 레벨을 사용하라.

- 관리자에게 이메일을 보낼 정도의 가치가 있는 오류를 기록할 경우 ERROR 레벨을 사용하는 것을 권장한다.
- 예외가 발생하는 경우, 문제를 해결할 수 있는 정보를 최대한 많이 기록하라.

### 27.3.3 Log Lower-Priority Problems With WARNING

잠재적인 위험이 있고 드물게 발생하는 상황이면서 ERROR 레벨만큼 나쁜 경우가 아니라면 WARNING 레벨을 사용한다.

- 예를 들어 django-admin-honeypot을 사용하는 경우, 침입자의 로그인 시도를 이 수준으로 로깅할 수 있다.
- Django는 CsrfViewMiddleware의 여러 부분에서 해당 로그 레벨을 사용한다.

[[CsrfViewMiddleware source code]](https://docs.djangoproject.com/en/1.8/_modules/django/middleware/csrf/)_

### 27.3.4 Log Useful State Information With INFO

분석이 필요한 경우에 필요한 정보들을 해당 로그 레벨로 기록한다

- 다른 곳에서 기록되지 않는 중요한 구성 요소의 시작 및 종료
- 중요 이벤트에 대한 응답으로 발생하는 상태의 변화
- 권한 변경(e.g. 관리자 액세스 권한 부여)

### 27.3.5 Log Debug-Related Message to DEBUG

개발 중에 디버깅을 위한 print문을 넣는 것을 고려한다면 DEBUG나 INFO 레벨의 로그를 사용하라. 프로젝트 전체에 print 문을 뿌리면 기술 부채가 발생한다.

- 웹 서버에 따라, 잊어버린 print 문이 사이트를 다운시킬 수 있다.
- print 문은 기록되지 않는다.
- Python3로 변경하는 경우, `print IceCream.objects.favorite()`와 같은 구버전의 print 문이 문제를 일으킨다.

print 문과 달리 로깅을 통해 다양한 보고 레벨을 설정할 수 있고, 다양한 응답 방법을 선택할 수 있다.

- DEBUG 레벨의 로그를 코드에 작성하고 남겨둘 수 있으며, Production 환경으로 코드를 옮기는 경우 어떠한 작업도 걱정할 필요 없다.
- 이메일, 로그파일, 콘솔 및 stdout과 같은 응답 방법이 있다. 심지어 Sentry와 같은 어플리케이션에 HTTP 요청을 통해 보고할 수 있다.

## 27.4 예외를 캐치하는 경우 Traceback 기록

- Logger.exception()은 자동으로 ERROR 레벨의 traceback 및 로그를 포함한다.
- 다른 로그 레벨의 경우, exc_info kwarg를 사용하라.

## 27.5 로깅을 사용하는 모듈 하나당 하나의 로거 사용

모듈에서 로그를 사용할 때, 다른 모듈의 로거를 가져오거나 재사용하지 마라. 예제와 같이 로거를 사용하면 필요한 특정 로거를 켜고 끌 수 있게 해준다.
예를 들어, Production 환경에서 로컬에서 복제할 수 없는 이상한 문제가 발생하는 경우, 문제가 발생하는 모듈에 대해서만 DEBUG 로깅을 임시로 설정할 수 있다.

## 27.6 순환하는 파일에 Local 기록

INFO 이상의 로그를 디스크에 순환하는 파일로 기록하는 것을 권장한다. 디스크 상의 로그 파일은 네트워크가 중단되거나, 메일을 보낼 수 없는 경우에 유용하다.

일반적인 방법은 UNIX logrotate 유틸리티를 logging.handler.WatchedFileHandler와 함께 사용하는 것이다.

## 27.7 다른 로깅 팁들

- [로깅 관련 Django 설명문서](https://docs.djangoproject.com/en/1.11/topics/logging/)
- 디버깅하는 동안엔 DEBUG 레벨의 Python 로거를 사용하라.
- DUBUG 레벨에서 테스트를 실행한 후, INFO 및 WARNING 레벨에서 다시 실행하라. 보이는 정보의 감소는 3rd-party 라이브러리에 대한 폐기 결정을 내리는데 도움이 될 수 있다.
- 최대한 빨리 로깅을 추가해라. 사이트가 고장나는 경우 우리가 기록한 로그에 감사할 것이다.
- ERROR 또는 그 이상 레벨의 이벤트가 발생할 때 이메일을 보내두면, 유용하게 사용할 수 있다.

## 27.8 필수로 읽어야 하는 자료

- https://docs.djangoproject.com/en/1.11/topics/logging/ 
- https://docs.python.org/3/library/logging.html
- https://docs.python.org/3/library/logging.config.html

## 27.9 유용한 3rd-Party tool

- Sentry: 오류 집계
- Opbeat: 어플리케이션의 오류와 성능 문제를 추적. Sentry의 기능 중 일부 제공하고 성능 모니터링도 지원함.
- Loggly: 간소화된 로그 관리 및 쿼리 툴 제공

## 27.10 요약

- Django는 Python과 함께 제공되는 풍부한 로깅 기능을 쉽게 이용할 수 있다.
- 핸들러 및 분석툴과 로깅을 결합하면, 진정한 힘을 얻게된다.
- 로그를 사용하여 프로젝트의 안정성과 성능을 향상시킬 수 있다.
