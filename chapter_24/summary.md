# 24. Finding and Reducing Bottlenecks

## 24.1 정말 신경써야하는가?

- 서툰 최적화는 지양
- 만약 사이트가 작은 규모이고, 페이지 로딩이 잘 된다면 신경쓰지 않아도 됨
- 물론 사용자가 꾸준히 늘고 있거나 유명 브랜드와의 제휴 를 체결할 예정이라면 신경써야 함

## 24.2 Speed Up Query-Heavy Pages

- 많은 쿼리, 의도와 다르게 느리게 작동하는 쿼리 등으로 인한 병목을 줄이는 방법
- [Django 공식 문서 : DB 접속 최적화](https://docs.djangoproject.com/en/1.11/topics/db/optimization/)

### 24.2.1 Find Excessive Queries With Django Debug Toolbar

`django-debug-toolbar` 활용

#### 확인할 병목

- 중복 쿼리
- 예상보다 많이 발생하는 쿼리
- 느린 쿼리

#### Links

- [django-cache-panel](https://github.com/lincolnloop/django-cache-panel)
- [django-extensions](https://github.com/django-extensions/django-extensions)
- [silk](https://github.com/jazzband/django-silk)

### 24.2.2 Reduce the Number of Queries

- related field 사용 시 `select_related`, `prefetch_related` 활용
- 템플릿에서 중복 쿼리를 실행하는 경우 해당 쿼리를 뷰로 이동
- 캐시 활용
  - 캐시 적용 후 쿼리 갯수 확인 테스트 [Django 공식문서 : Test (TransactionTestCase.assertNumQueries)](https://docs.djangoproject.com/en/1.11/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries)
  - `django.utils.functional.cached_property` 데코레이터 활용

### 24.2.3 Speed Up Common Queries

- 인덱스 활용 : 변환된 raw 쿼리를 확인하여 인덱스 필드 정하기 (EXPLAIN ALANLYZE/EXPLAIN 활용)
- query plan 확인하기
- 데이터베이스의 slow query logging 기능 활용
- django-debug-toolbar에서 느린 쿼리 확인

#### 쿼리 재 작성 Tip

- 적은 쿼리 결과가 반환되도록 쿼리 재작성
- 인덱스를 효과적으로 활용할 수 있도록 데이터 재구성
- raw SQL 활용

### 24.2.4 Switch ATOMIC_REQUESTS to False

- 트랜잭션에서 병목이 일어난다면 `ATOMIC_REQUESTS`를 `False`로 !
- 대부분의 프로젝트에서는 신경쓰지 않아도 될 정도임

## 24.3 Get the Most Out of Your Database

### 24.3.1 Know What Doesn’t Belong in the Database

- 로그
  - 데이터가 커지면 DB 성능 느려짐
  - 서드파티 서비스([Splunk](), [Loggly]())나 NoSQL 추천
- 일시적(Ephemeral) 데이터
  - 자주 re-writing 하는 데이터
  - django.contrib.sessions, django.contrib.messages
- 바이너리 데이터

### 24.3.2 Getting the Most Out of PostgreSQL

- 프로덕션 환경에서 제대로 세팅되어야 함

#### Links

- http://wiki.postgresql.org/wiki/Detailed_installation_guides
- http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server
- http://www.revsys.com/writings/postgresql-performance.html
- http://www.craigkerstiens.com/2012/10/01/understanding-postgres-performance/
- http://www.craigkerstiens.com/2013/01/10/more-on-postgres-performance/
- [PostgreSQL 9.0 High Performance](https://amzn.to/1fWctM2)

### 24.3.3 Getting the Most Out of MySQL

- 마찬가지로 프로덕션 환경에서는 제대로 세팅되어야 함

#### Links

- [The Unofficial MySql Optimizer Guide](http://www.unofficialmysqlguide.com/)
- [High Performance MySQL](https://amzn.to/188VPcL)

## 24.4 Cache Queries With Memcached or Redis

- 간단하게 세팅가능
- [Django 공식 문서 : 캐시](https://docs.djangoproject.com/en/1.11/topics/cache/)
- [django-redis-cache 패키지](https://github.com/niwinz/django-redis)

## 24.5 Identify Specific Places to Cache

- 쿼리를 가장 많이 포함하고 있는 뷰/템플릿
- 가장 많이 호출되는 URL
- 캐시 삭제 시점

## 24.6 Consider Third-Party Caching Packages

#### 기능

- 쿼리셋 캐싱
- 캐시 초기화 세팅/메커니즘
- 다양한 캐시 백엔드
- 대안 혹은 캐시에 대한 경험적 접근

#### Django 패키지

- django-cache-machine
- johnny-cache
- django-cachalot
- [다양한 옵션들](https://www.djangopackages.org/grids/g/caching/)

*서드파티 캐싱 라이브러리가 항상 답은 아니다*

## 24.7 Compression and Minification of HTML, CSS, and JavaScript

#### 압축, Minification

- Django에서 처리
  - GZipMiddleware
  - {% spaceless %} 템플릿 태그
  - WSGI 미들웨어
- 웹서버가 처리
  - Django에서 처리 시 문제점 : 압축과정 자체가 병목이 될 수 있음가 
  - 웹서버가 외부로 전달되는 컨텐츠를 압축하는 것이 더 나음
- 서드 파티 Django 라이브러리로 압축가 Minification을 미리 처리

#### 참고

- Apache and Nginx compression modules
- django-pipeline
- django-compressor
- django-htmlmin
- [Django’s built-in spaceless tag](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/spaceless)
- djangopackages.org/grids/g/asset-managers/

## 24.8 Use Upstream Caching or a Content Delivery Network

#### Upsteam Cache 사용

- [varnish](http://varnish-cache.org/)

#### CDN 이용

- [Fastly](), [Akamai](), [Amazon Cloudfront]()

## 24.9 추가 자료

- [YSlow’s Web Performance Best Practices and Rules](http://developer.yahoo.com/yslow/)
- [Google’s Web Performance Best Practices](https://developers.google.com/speed/docs/best-practices/rules_intro)
- [High Performance Django](https://highperformancedjango.com/)
- [David Cramer의 블로그](http://justcramer.com/)
- [DjangoCon, Pycon 자료](http://lanyrd.com/search/?q=django+scaling)