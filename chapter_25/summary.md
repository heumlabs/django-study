# 25. 비동기 태스크 큐

- 비동기 태스크 큐(asynchronous task queue)란 태스크가 실행되는 시점이 태스크가 생성되는 시점과 다르고
태스크의 생성 순서와도 연관 없이 실행되는 작업을 의미한다.

> django 에서는 '태스크 큐' 와 '비동기 태스크 큐' 모두 비동기 태스크 큐를 의미한다.

- 용어 정의
    - **broker**: task 저장소. django 에서는 RabbitMQ와 redis가 일반적으로 쓰인다.
    - **producer**: 나중에 실행될 task 를 queue에 넣는 코드. django 프로젝트의 application 코드를 말한다.
    - **worker**: broker에서 task를 가져와서 실행하는 코드. 일반적으로 하나 이상의 worker가 있다.
    각 worker는 데몬 형태로 실행되며 관리를 받는다.
    - **serverless**: 보통 **AWS Lambda**와 같은 서비스에서 제공받는다.
    서버쪽 로직은 우리가 작성하지만, 3rd party에서 관리되는 stateless compute container에서 event-trriger되어 실행
    일상생활 예에서는 Daniel과 Audrey가 제3자 서비스를 사용하여 주문을 받은 후 작업 하는 것이 이에 해당

## 25.1 Task Queue가 필요한가?

- 상황에 따라 다르다. (아래 내용 참고)
    - **`결과에 시간이 걸리는 작업`**은 Task Queue를 이용해야 한다.
    - **`사용자에게 바로 결과를 제공해야하는 작업`**은 Task Queue를 이용하지 말아라.

| Issue                                    | Use Task Queue? |
| ---------------------------------------- | --------------- |
| 대량 이메일 발송                                  | yes             |
| 파일들을 수정할 때 (이미지를 포함한)                  | yes             |
| 대량의 데이터를 API로부터 받아올 때                  | yes             |
| 대량의 record를 table에 insert 하거나 update 할 때 | yes             |
| 긴 시간을 필요로 하는 계산을 수행할 때                | yes             |
| webhook을 받거나 보낼 때                          | yes             |
| 사용자의 프로파일을 변경 할 때                      | no              |
| 블로그나 CMS에 글을 더할 때                        | no              |

- 모든 케이스에는 항상 사이트 트래픽에 따라 달라질 수 있다.
    - 트래픽이 적은 경우 위 내용과 상관없이 task queue를 이용할 필요가 없다.
    - 트래픽이 많은 경우 모든 작업에 task queue가 필요하다.

## 25.2 Task Queue 소프트웨어 선택하기

- [Celery](http://www.celeryproject.org/)
    - **장점**: Django와 python 표준, 유연하고 기능이 많으며 High volume에서 잘 동작함
    - **단점**: 설치하기 어려우며, 기초적인 부분 외에는 러닝커브가 있음

- [DjangoChannels](https://channels.readthedocs.io/)
    - **장점**: 사실상 django 표준, 유연하고 사용하기 편하며, django에서 websocket을 사용할 수 있음
    - **단점**: Redis만 용해야 하며, retry mechanism이 없음

- [AWSLambda](https://aws.amazon.com/ko/lambda/)
    - **장점**: 유연, 확장 가능성, 설치가 쉬움
    - **단점**: API call이 느릴 수 있으며, 추가로 logging system이 필요하고, 복잡도가 올라감

- [Redis-Queue](http://python-rq.org/), [Huey](https://github.com/coleifer/huey), 그 밖의 django 친화적인 queue
    - **장점**: 상대적으로 설치가 쉽고, Celery에 비해 적은 메모리를 사용함
    - **단점**: 기능이 별로 없고, 보통 Redis만 사용해야 하며 커뮤니티가 활성화 되어있지 않음

- [django-background-tasks](https://github.com/arteria/django-background-tasks)
    - **장점**: 아주 쉬운 설치, 쉬운 사용법, windows에서도 동작하며, 소규모 작업에 사용하기 좋음
    - **단점**: medium-to-high volume에서 사용하기 부적합

- 저자의 경험에 따른 일반적인 rule
    - 시간이 허락한다면 모든 비동기 프로세스는 AWS Lambda와 같은 Serverless 시스템으로 이동해라.
    - Serverless에 대한 API 호출에 이슈가 발생할 경우, Celery 태스크로 캡슐화해라.
    저장의 경우 AWS Lambda에서 대량의 API를 호출 할 때만 문제가 발생했다고함.
    - websocket의 경우 Django Channels 사용해라.
    The lack of retry mechanism forces you to invent things that Celery provides out-of-the-box.
    - 보안과 성능상의 이유로 사용자가 정의한 URL에 대한 API 호출은 task queue를 이용한다.

- 자신의 경험과 지식에 기반을 두고 어떠한 task queue 를 사용할 지 정해야한다. 
    - celery를 잘 다룬다면 소규모 프로젝트에 사용해도 좋다.
    - 대부분의 Serverless 시스템은 디스크 드라이브 공간에 용량제한이 있다.(예: AWS Lambda는 512MB로 제한)
    이는 비디오의 코드 변환과 같은 대용량 파일을 조작하거나 특정 라이브러리를 사용할 때 문제가 될 수 있다.
    이러한 경우 타사 서비스를 사용하거나 Celery를 이용해라.
    - 재시도 mechanism을 작성할 경우 Django Channel's Generic Consumers 이 좋다. 
    다만 예상보다 크고 복잡한 작업이라는 점을 명심해라.
    - Redis Queue와 Huey와 같은 queue는 Celery보다 설치가 쉽다.
    그러나 Cookiecutter Django와 같은 프로젝트 템플릿을 사용하면 이를 이용할 수 없다.

## 25.3 Task Queue의 실전 방법론

- 여기서 설명하는 방법론의 이점은 각 task 기능이 이식성이 좋게 하는 것이다.
예를 들어 재시도 메커니즘이 없어 Django Channels를 Celery로 바꿀 때 좋다.

### 25.3.1 Task를 View처럼 다루자

- 앞서 view 를 작성할 때, 메서드와 함수를 다른 곳에서 호출하여 view를 가능한 작게 구성하도록 권장했다.
Task를 작성할 때도 이와 같은 방법을 적용하도록 하자.

- Serverless 코드에서도 마찬가지다. AWS Lambda 함수에 많은 로직을 넣는 대신, 패키지를 만들자. 디버깅이 쉬워진다.

### 25.3.2 Task 또한 리소스를 이용한다.

- Task 또한 리소스와 메모리를 필요로한다. 과도한 리소스를 사용하는 Task는 사이트에 문제를 야기 할 수 있으므로 단순 명료하게 코드를 작성하고,
리소스를 낭비하지 않는 방향으로 코드를 작성해라.

- Serverless(AWS Lambda) 또한 무료가 아니며, 과도한 리소스를 사용할 경우 엄청난 청구서를 받게 될것이다.

### 25.3.3 json으로 변경 가능한 value만 Task 함수에 전달해라.

- integers, floats, strings, lists, tuples and dictionaries 만 전달해라. 복잡한 objects 절대 전달하지 말아라.

- 그 이유는 다음과 같다.
    - ORM instance의 경우 race condition(경합상황) 문제가 발생할 수 있다. 대신 primary key를 사용하자.
    - 복잡한 형태의 object를 함수로 전달하면 시간과 메모리가 더 많이 든다.
    이것은 Task Queue를 이용하여 얻으려던 장점과 정면으로 대치된다.
    - 디버깅이 쉽다.
    - json으로 직렬화된 것만 허용하는 task queue가 있다.

### 25.3.4 결과가 항상 같도록 Task 를 작성해라.

- Task 를 여러번 실행하여도 항상 같은 결과를 반환해야한다. 왜냐하면 성공한 task라 하여도 항상 재시도 가능성은 열려있다.
- [Pure Funtion(순수함수)](http://minsone.github.io/programming/pure-function)

### 25.3.5 중요한 데이터는 Queue 에 보관하지 말아라.

- Django Channels를 제외하고 다른 Task Queue는 재시도 메커니즘이 있지만 때때로 실패할 때가 있다.

- 해결방법은 작업상태를 추적하는 것이다.

- [위 내용에 대한 좋은 article](https://www.caktusgroup.com/blog/2016/10/18/dont-keep-important-data-your-celery-queue/)

### 25.3.6 Task와 Worker의 모니터링 방법을 알아둬라

- [Celery Flower](https://pypi.org/project/flower/)

### 25.3.7 로깅!

- Task Queue 는 뒤에서 진행되어 어떤 상태인지 정확히 파악하기 어렵다. 로깅(27장) 및 Sentry와 같은 도구가 유용하게 쓰일 수 있다.
- 에러가 발생하기 쉬운 Task는 함수내에 꼭 로그를 남겨라.
- Serverless Task를 사용하는 경우 꼭 Sentry를 써라. 필수임!!.

### 25.3.8 Backlog 모니터링하기

- 트래픽이 증가하는데 worker가 충분하지 않다면 worker를 늘려라.
- Serverless Task에는 적용되지 않는다.

### 25.3.9 죽은 Task는 주기적으로 지워라.

- 다양한 이유로 이러한 현상은 발생할 수 있다. 점점 늘어나면 시스템 공간을 차지하게 되므로 주기적으로 삭제하자.

### 25.3.10 필요없는 결과는 무시해라.

- Task가 완료되면 broker는 성공 또는 실패 여부를 기록하도록 설계되어 있다.
- 통계 목적으로 유용하지만 작업의 결과가 아니므로 이러한 기능은 꺼라.

### 25.3.11 Queue의 에러 핸들링 이용하기

- Task가 실패할 경우 Task Queue 소프트웨어가 어떻게 작동하는지 살펴보고 다음 값들을 어떻게 세팅하는지 확인해라.
    - Task 최대 재시도 횟수(Max retries for a task)
    - 재시도 전 지연 시간(Retry delays)
- 저자의 경우 task가 실패하면 재시도를 하기전 적오도 10초 이상 기다린다. 재시도 할 때 마다 점진적으로 시간을 늘려라. (자연적으로 복구 될 시간을 갖기 위해)

### 25.3.12 사용하는 Task Queue 소프트웨어의 기능을 익혀라.

- Celery, Django Channels 및 Redis Queue를 사용하면 여러 Queue를 정의 할 수 있다.
실제로 Celery는 다른 소프트웨어 패키지가 가지고 있지 않은 라우팅 기능을 갖추고 있다.

- 저자는 AWS Lambda를 선호하지만 아직 Celery를 쓰는 이유는 잘 컨트롤 할 수 있기 때문이다.

## 25.4 Task Queue 참고 자료

- https://www.vinta.com.br/blog/2016/database-concurrency-in-django-the-right-way/
- https://www.fullstackpython.com/task-queues.html
- https://www.slideshare.net/bryanhelmig/task-queues-comorichweb-12962619
- https://github.com/carljm/django-transaction-hooks

- Celery 참고자료
    - http://www.celeryproject.org/
    - https://denibertovic.com/posts/celery-best-practices/
    - https://pypi.org/project/flower/
    - https://wiredcraft.com/blog/3-gotchas-for-celery
    - https://www.caktusgroup.com/blog/tags/celery/

- Django Channels
    - https://channels.readthedocs.io/en/latest/
    - https://github.com/django/channels