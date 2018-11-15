# 18. Tradeoffs of Replacing Core Components

Django의 Core Part를 교체하는 일을 해야할까?

- Short Answer
  - 하지 마라
  - [인스타그램 CEO 인터뷰](http://bit.ly/2pZxOBO)
- Long Answer : 가능하지만 정말 가치가 있는지 아래의 조건들을 살펴보아라
  - 3rd-party Django Package를 포기할 수 있다면
  - Django Admin을 포기해도 괜찮다면
  - 이미 Django core component로 많은 노력을 했지만 벽에 막혔다면
  - 이미 코드를 분석하여 문제의 근본원인을 파악하고 고쳤다면
  - Caching, Denormalization 등의 옵션을 다 살펴보았다면
  - Your project is a real, live production site with tons of users. In other words, you’re certain that you’re not just optimizing prematurely.
  - You’ve looked at and rejected adopting a Service Oriented Approach (SOA) for those cases Django has problems dealing with.
  - You’re willing to accept the fact that upgrading Django will be extremely painful or impossible going forward.

## 18.1 The Temptation to Build FrankenDjango

### 유행 1. 성능 문제로 데이터베이스/ORM을 NoSQL 데이터베이스로 교체하고 관련 ORM을 교체!

- Not okay
  - 지금은 아니지만, 미래에 많은 사용자가 있을 것이다.
- Okay (많~은 고려를 했다면 OK)
  - 이미 많은 사용자가 있고
  - Index, Query 최적화, Caching 등 할 수 있는 일의 한계에 도달하였고
  - Postgres cluster의 한계에 도달하고 있고
  - 많은 연구를 했고
  - CAP 정리에 대해 알고 있고

### 유행 2. 데이터 처리 문제로 데이터베이스/ORM을 NoSQL 데이터베이스로 교체하고 관련 ORM을 교체!

- Not okay
  - SQL 구림! MongoDB 같은 문서 기반 데이터베이스로 간다!
- Okay (많~은 고려를 했다면 OK)
  - PostgreSQL의 HSTORE 데이터타입이 MongoDB 데이터 저장 시스템과 거의 유사하지만, 우리는 MongoDB에서 기본적으로 제공되는 MapReduce 기능을 사용하고 싶다.

### 유행 3. Django의 템플릿 엔진을 Jinja2, Mako 등으로 교체!

- Not okay
  - Hacker News 보니깐 Jinja2가 더 빠르다고 함! Caching 이나 최적화는 모르지만 Jinja2로 간다!
  - 파이썬 모듈에 로직이 있는게 싫어! Logic은 템플릿 안으로 간다!
- Okay (많~은 고려를 했다면 OK)
  - Google에서 색인할 수 있도록 만들어진 1MB가 넘는 HTML 페이지를 생성하는 View가 몇 개 있습니다... Django는 여러 개의 템플릿 언어를 지원하기 때문에 1MB 이상의 페이지를 Jinja2로,나머지는 Django 템플릿 언어로 렌더링합니다.

## 18.2 Non-Relational Databases vs. Relational Databases

### 18.2.1 Not All Non-Relational Databases Are ACID Compliant

- ACID
  - 원자성
  - 일관성
  - 고립성
  - 지속성


### 18.2.2 Don’t Use Non-Relational Databases for Relational Tasks

관계형 데이에 비관계형 Database를 쓰지마라

### 18.2.3 Ignore the Hype and Do Your Own Research

- 충분히 사례나 문제를 조사하고 취미 프로젝트에서 테스트 해보아라. (기본 프로젝트 인프라를 변경하기 전에)
- 교훈들
  - [Learn to stop using shiny new things and love MySQL](https://medium.com/@Pinterest_Engineering/learn-to-stop-using-shiny-new-things-and-love-mysql-3e1613c2ce14)
  - [Why MongoDB Never Worked Out at Etsy](http://mcfunley.com/why-mongodb-never-worked-out-at-etsy)


### 18.2.4 How We Use Non-Relational Databases With Django

- Non-relatioal Data Store : Cache, Queue, 혹은 비정규화가 필요한 데이터
- Relational Data Store : 오래 저장되는 정규화된 데이터 혹은 비정규화된 데이터 일부 (PostgreSQL의 array나 HStore 필드)

## 18.3 What About Replacing the Django Template Language?

- 큰 사이즈의 렌더링된 콘텐츠를 제외하고는 Django 템플릿 언어를 사용
- 하지만 이제 Django에서 템플릿 언어를 대체할 수 있도록 기본적으로 지원
- 15장 참고
