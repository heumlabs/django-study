# 6. 모델 best practice

모델은 많은 Django proejct의 밑바탕이다.  
생각없이 Django 모델을 사용하게 된다면 많은 문제를 직면하게 될 것이다.

> **Package Tip**  
> `django-모델-utils`: `TimestampedModel`과 같이, 흔히 사용하는 패턴의 모델을 제공한다.  
> `django-extensions`: `INSTALLED_APPS`에 등록된 모든 app의 모델을 자동으로 불러와주는 `shell_plus` 및 여러기능을 제공한다. 하지만 작은 단위에 초점이 맞춰진 우리의 선호와는 달리 너무 많은 기능을 가지고있다.

## 6.1 기본
### 6.1.1 많은 모델을 갖고 있는 App 분리하기

만약 한 app에 20개가 넘어가는 모델이 있다면 하나의 앱이 너무 많은 기능을 하는 것이다.

하나의 app이 5개 이하의 모델을 갖도록 작은 단위로 분리하자.

### 6.1.2 모델 상속에 주의하기

Django에서, 모델 상속은 까다로운 주제다.

Django는 3가지 방법의 모델 상속을 제공한다.

- 추상화 클래스
- 다중 테이블 상속
- 프록시 모델

#### 각 모델 상속의 특징 및 장단점

- **상속을 사용하지 않는 모델**
    - 특징: 공통된 필드를 갖는 모델이 있다면, 모델마다 공통 필드를 정의한다
    - 장점: 해당 모델이 어떻게 데이터베이스에 매핑되었는지 한눈에 파악하기가 쉽다.
    - 단점: 여러 모델에 중복된 필드가 많아지는 경우, 유지보수가 어려워진다.
- **추상화 클래스를 이용한 상속**
    - 특징: 데이터베이스 테이블은 상속받은 모델만 생성된다.
    - 장점: 공통된 필드에 대해 반복적으로 타이핑하지 않아도 된다. 다중 테이블 상속으로 인해 생기는 추가 테이블과의 결합으로 발생하는 오버헤드가 없다.
    - 단점: 부모 클래스를 단독으로 사용할 수 없다.
- **다중 테이블 상속**
    - 특징: 각 모델별로 테이블이 생성되며, 암묵적인 `OneToOneField`로 부모와 자식이 연결된다.
    - 장점: 각 모델별로 테이블이 생성되기 때문에 부모 또는 자식 모델 어느쪽에서든 쿼리가 가능해진다. 또한 부모 object에서 자식 object를 찾을 수 있다(`parent.child`)
    - 단점: 자식 테이블의 쿼리는 모든 상위 테이블과의 join이 필요해지기 때문에 상당한 오버헤드 가 추가된다.
    - [[example]](https://godjango.com/blog/django-abstract-base-class-multi-table-inheritance/)
- **프록시 모델**
    - 특징: 원본 모델의 테이블만 생성된다. (추상화랑 반대)
    - 장점: 전혀 다른 기능을 하는 별칭을 모델이 가지게 할 수 있다.
    - 단점: 그렇다고 해서 원본 모델의 필드를 변경할 수 있는건 아니다.

> 다중 테이블 상속은 때때로 `접합 상속`으로 불리며, 이 책의 저자나 개발자들 사이에서 안좋은 방법으로 간주된다.  
> 사용하지 않는 것을 강력히 추천한다.

#### 상속을 사용하는 룰

- 두 개 정도의 모델에서 한두 개의 필드가 중복되는 경우, 상속이 필요하지 않다. 각각의 모델에 필드를 정의하자.
- 모델 사이에 충분히 필드가 중복되는 경우, 반복되는 필드를 유지보수하려면 큰 혼동이 따른다. 이런 경우에는 추상화 클래스를 이용하도록 모델을 리팩토링한다.
- 프록시 모델은 잘 쓰면 편리하다. 하지만 다른 상속 방법들과는 완전히 매우 다른 방식임을 명심하자.
- 다중테이블 상속은 굉장히 헷갈리며 오버헤드를 발생시킨다. 필요하다면 모델 간에 명시적인 `OneToOneField`나 `ForeignKeys`를 사용하여 join을 조절할 수 있도록 한다.

### 6.1.3 모델 상속 예제: TimeStampedModel

Django의 모델에서 created, modified 필드를 추가하는 경우가 많다.

```
class TimeStampedModel(Models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Flavor(TimeStampedModel):
    title = models.CharField(max_length=200)
```

모델의 Meta class에 `abstract=True`를 선언하게 되면, 테이블이 생성되지 않는다.

위의 경우, `Flavor` 모델의 테이블만 생성된다.

> 만약 `abstract=True`를 선언하지 않았다면 다중 테이블 상속이 되어, `TimeStampedModel` 테이블과 `Flavor` 테이블이 각각 생성되며 `Flavor` 테이블은 created/modified 필드를 처리하기 위해암묵적인 외래 키를 갖게된다. 때문에 `Flavor` 모델에 대한 참조는 두 테이블에 영향을 미치게 된다.


## 6.2 데이터베이스 마이그레이션

### 6.2.1 마이그레이션 생성 팁

- 새로운 앱이나 모델을 생성한 경우엔 `manage.py makemigrations` 명령어를 호출한다.
- 생성된 마이그레이션을 적용하기 전에, 먼저 마이그레이션 파일의 코드를 검사하자.
- `sqlmigrate` 명령어를 사용해 마이그레이션이 실행될 때의 SQL문을 검사할 수 있다.
- `django.db.migrations` 스타일이 아닌 써드파티 앱에 대해 마이그레이션은 `MIGRATION_MODULES` 세팅을 이용한다.
- 마이그레이션 파일의 수가 많아져 관리가 힘들어지면 `squashmigrations` 명령어를 사용하자.
- 마이그레이션을 하기전 데이터 백업은 필수다.

### 6.2.2 마이그레이션에 Python 함수 및 커스텀 SQL 추가

`django.db.migrations`로는 외부 구성요소나 데이터의 복잡한 변경을 예상할 수 없다.

그런 경우 migration이 실행될 때 동작하는 python code나 커스텀 SQL을 작성하는 방법을 알아보는 것이 유용하다.

[[RunPython class docs]](https://docs.djangoproject.com/en/1.11/ref/migration-operations/#runpython)  
[[RunSQL class docs]](https://docs.djangoproject.com/en/1.11/ref/migration-operations/#runsql)

## 6.3 RunPython의 일반적인 장애 해결 방법

### 6.3.1 커스텀 모델 매니저 메서드 사용하기

RunPython에서 커스텀 모델 매니저의 메서드를 이용하여 필터를 하거나 제외시키거나, 생성하고 변경하고 싶은 경우가 있을 것이다.  
이러한 경우 `use_in_migrations = True`를 커스텀 모델 매니저에 추가해준다.

### 6.3.2 커스텀 모델 메서드 사용하기

`django.db.migrations`가 model을 serialize하기 때문에, 커스텀 모델 메서드는 마이그레이션을 실행할 때 사용할 수 없다.

[[Historical models docs]](https://docs.djangoproject.com/en/1.11/topics/migrations/#historical-models)

> 만약 `save()`나 `delete()` 메서드를 override를 한 경우, RunPython은 해당 메서드를 호출하지 않는다. 주의 요망!!

### 6.3.3 RunPython.noop을 사용하여 일을 줄이기

RunPython을 이용하여 마이그레이션을 할 경우, 마이그레이션을 취소하기 위한 `reverse_code`는 필수로 작성되야한다.

하지만 이런 `reverse_code`는 작성하는게 불가능하거나 의미가 없다. 이럴때 `reverse_code` 작성 대신 사용하는게 `RunPython.noop`이다.

예제 코드에서 `Cone` 모델을 추가하였고, 각 scoop에 cone을 추가하기 위해 `add_cones` 함수를 작성하였다. 이 마이그레이션을 취소한다면 `migrations.CreateModel.database_backward`로 인해 cone.cone 테이블을 제거하게 되고, 생성된 cone들은 제거가된다. 이미 제거된 cone 때문에 `reverse_code`를 작성하는건 무의미하다.

즉, 이럴때 `reverse_code` 대신 `RunPython.noop`을 사용하면 된다.

### 6.3.4 배포와 마이그레이션 관리

- 배포 전에 마이그레이션을 롤백할 수 있는지 확인해야한다. 이전 상태로 롤백할 수 없다면 버그 추적이나 대규모 프로젝트의 배포에 굉장히 힘들어진다.
- 프로덕션 환경에 데이터가 많다면, 그와 비슷한 규모의 스테이징 서버에서 충분한 테스트를 하자.
- MYSQL을 사용하는 경우
    - 스키마를 변경하기 전에 백업한다.
    - 변경사항을 적용하기 전에 읽기전용 모드로 설정한다.
    - 주의하지 않는 경우 스키마 변경에 몇 시간이 걸릴 수 있다.

## 6.4 Django 모델 디자인

### 6.4.1 정규화 시작하기

Django 모델을 설계할 때는 항상 모델의 정규화로부터 시작한다. 다른 모델에 이미 저장된 데이터를 모델에 포함해서는 안 된다.

이 단계에서는 관계 필드를 자유롭게 사용한다. 너무 일찍 정규화하지 마라!

[[Database normalization]](https://en.wikipedia.org/wiki/Database_normalization)  
[[Relational database design]](https://en.wikibooks.org/wiki/Relational_Database_Design/Normalization)

### 6.4.2 캐시와 비정규화

올바른 위치에 캐시를 설정하면 모델을 비정규화하는 문제를 줄일 수 있다.  
(Chapter 24에서 자세히 알아본다.)

### 6.4.3 비정규화는 반드시 필요한 경우에만

비표준화는 프로젝트에서 문제를 일으키는 것에 대한 만병통치약처럼 보일 수 있다.  
그러나 이 프로세스는 프로젝트에 복잡성을 가중시키고 데이터 손실 위험을 크게 높일 수 있다.  
비정규화를 하기 전 캐시를 먼저 살펴보도록 하자.  
(Chapter 24에서 자세히 알아본다.)

### 6.4.4 어떤 경우에 Null과 Blank를 사용할까?

(책 참조)

### 6.4.5 어떤 경우에 Binary Field를 사용할까?

Binary Field는 raw binary data 또는 byte를 저장하는 필드이다.
필터나 제외, 기타 SQL 액션들이 이 필드에 대해 실행되지 않는다.

#### 사용처

- 메시지팩 형식의 콘텐츠
- 원본 센서 데이터
- 압축된 데이터

Binary 데이터는 크기가 클 수 있고, 이로 인해 데이터베이스가 느려질 수 있다.

> **주의**: 해당 필드에서 직접 파일을 서비스 하지 않는다!  
> 데이터베이스의 읽기/쓰기 속도는 파일 시스템의 읽기/쓰기 속도보다 느리다.
> 백업에 들어가는 리소스가 점점 증가한다.
> 파일에 접근하기 위해 Django app과 DB를 모두 거쳐야한다.


### 6.4.6 GenericRelations 피하기

GenericRelation은 한마디로 제약이 없는 외래키(GenericForeignKey)를 이용해 테이블을 다른 테이블에 바인딩 하는 것이다.

**GenericRelations 장단점**

- 장점
    - 하나의 모델이 수많은 모델과 상호작용을 해야할 때 쉽게 앱을 만들 수 있다.
- 단점
    - 두 모델 사이에 인덱싱이 존재하지 않아, 쿼리 속도가 떨어진다.
    - 테이블이 다른 테이블을 참조할 때, 존재하지 않는 레코드를 참조하여 데이터의 손상이 발생할 수 있음.

**그렇다면 어떻게 해야하는가?**

- Generic relations 및 GenericForeignKey의 사용을 피하도록 한다.
- 만약 필요하다면, PostgreSQL 만의 새로운 필드를 사용하여 모델 디자인을 개선해본다.
- 꼭 사용해야하는 경우에는 써드파티 앱을 이용하도록 한다.

### 6.4.7 Choice와 Sub-Choice 모델 Constants 만들기

choice의 가장 이상적인 패턴은, 모델이 해당 choice를 가지게 하는 것이다. 이런 방식은 choice constants에 쉽게 접근을 가능하게 하고, 개발을 더욱 쉽게 할 수 있도록 해준다.

### 6.4.8 Enum을 사용하여 더 나은 모델 choice 만들기

[[Enum Library]](https://pypi.python.org/pypi/enum34)


### 6.4.9 PostgreSQL의 특별한 Field들: 어떤 경우에 Null과 Blank를 사용할까?

(책 참조)

## 6.5 모델 `_meta` API

#### `_meta` API를 사용하는 경우는?

- 모델에 있는 필드의 목록을 가져오고 싶을 때
- 모델에 있는 특정 필드의 클래스를 가져오고 싶을 때
- 이후의 Django 버전에서도 이러한 정보를 얻는 방법을 유지시키고자 할 때

#### `_meta` API 사용 예시

- Django 모델을 검사하는 툴을 제작할 때
- 커스텀 Django form 라이브러리를 제작할 때
- Django Admin과 같이, 모델 데이터를 수정하거나 상호작용하는 툴을 제작할 때
- 시각화 또는 분석 라이브러리를 작성할 때 (예시: "foo"로 시작하는 필드에 대한 정보 분석)

[[Meta API docs]](https://docs.djangoproject.com/en/1.11/ref/models/meta/)

## 6.6 모델 매니저

모델 매니저는 Django ORM을 사용하여 모델을 쿼리할 때 데이터베이스와 상호작용을 할 수 있도록 해주는 인터페이스다.  
Django는 각 모델 클래스에 대해 기본 모델 매니저를 제공하지만, 자체 모델 관리자를 정의할 수 있다.

> **기본 모델 매니저 교체시 주의 사항**
> 
> - 추상화 클래스를 상속하여 생성된 모델은 추상화 클래스에서 선언된 모델 매니저를 같이 상속 받지만, 접합 상속 기반의 모델은 상속 받지 못한다.
> - 모델 클래스에 적용되는 첫 번째 매니저는 장고의 기본 모델 매니저이다. 커스텀 모델 매니저로 교체하면 기본값도 커스텀 모델 매니저로 변경된다. 이러한 경우 Queryset 재정의 하면 예상하지 못한 결과를 얻을 수 있다.

모델 클래스 안에서 `objects = models.Manager()`를 선언하면 모델 매니저를 교체할 수 있다.

[[Manager docs]](https://docs.djangoproject.com/en/1.11/topics/db/managers/)

## 6.7 거대 모델에 대한 이해

거대 모델이란 뷰나 템플릿에 데이터와 관련된 코드를 작성하는 것 대신, 로직을 모델 메서드, 클래스 메서드, 프로퍼티 그리고 매니저 메서드로 캡슐화 시킨 모델을 말한다.  
이러한 거대 모델의 장점은 모든 뷰나 태스크가 동일한 로직을 사용할 수 있다는 것이다.

하지만 이러한 거대모델이 꼭 좋은 것 만은 아니다.

모델에 모든 로직을 넣게 되면 크기가 점점 커지면서 `God Object`가 된다.  
문제점으로는 크기가 커지면서 코드를 이해하기 힘들어지고, 테스트와 유지보수가 어렵게 된다.

### 6.7.1 모델 행동 (이른바 Mixins)

모델 행동은 믹스인을 이용하여 구성 및 캡슐화된다.  
모델은 추상화 모델에서 로직을 상속받는다.

[[Django model behaviors by Kevin Stone]](http://blog.kevinastone.com/django-model-behaviors.html)

### 6.7.2 무상태 헬퍼 함수

- 로직을 모델과 분리시켜 유틸리티 함수로 만들면 독립적으로 사용이 가능하다.
- 독립적인 함수는 로직에 대한 테스트를 작성하기가 쉬워진다.
- 하지만 모델에 대한 상태를 알 수 없게 되므로, 더 많은 인자를 필요로 하게 된다.

### 6.7.3 모델 행동 vs 헬퍼 함수

둘 다 완벽하지 않다. 두 가지 모두 적절하게 사용하는 것이 현명하다.

모델 행동이나 헬퍼 함수를 적용하는 것은 굉장히 까다로운 일이기 때문에, 그에 앞서 기존의 거대 모델의 구성요소에 대한 테스트가 선행되어야한다.

## 6.8 요약

- 모델은 많은 Django proejct의 밑바탕이다. 반드시 신중하게 디자인하자.
- 정규화를 하자. 비정규화가 필요하다면 하기전에 먼저 다른 선택지를 모두 확인하자. (Raw SQL, Cache 등)
- 인덱스를 사용하는걸 잊지마라.
- 모델 상속을 사용한다면, 접합 상속보다는 추상화 클래스 상속을 사용하자.
- `null=True`, `blank=True`를 필드에 추가하고자 할 경우에는 책에 나와있는 내용을 참고해라.
- `django-model-utils`나 `django-extensions`를 사용하면 굉장히 편할 것이다.
- 거대 모델은 로직을 모델에 캡슐화 하는 방법이다. 하지만 언제든 `God object`가 될 수 있으니 주의하자!
