# 7. 쿼리와 데이터베이스 레이어

## 7.1 단일 객체에서 get_object_or_404() 이용하기

- 단일 객체를 가져와서 작업하는 View에서는 `get()` 대신 `get_object_or_404()`를 이용하자. (단, View에서만 사용)
- 예외 처리를 하지 않아도 됨

```python
# 1 
def test_view(request):
    try:
        company = Company.objects.get(pk=1)
    except Company.DoesNotExist:
        raise Http404("No MyModel matches the given query.")

# 2
from django.shortcuts import get_object_or_404

def test_view(request):
    get_object_or_404(Company, pk=1)
```

## 7.2 예외를 일으킬 수 있는 쿼리를 조심하자

`get_object_or_404()` 는 예외 처리를 할 필요 없음

### 7.2.1 ObjectDoesNotExist vs DoesNotExist

- `ObjectDoesNotExist` : 모든 모델 객체에 이용 가능
- `DoesNotExist` : 특정 모델만 이용 가능

```python
 from django.core.exceptions import ObjectDoesNotExist 

from flavors.models import Flavor
from store.exceptions import OutOfStock

# DoesNotExist
def list_flavor_line_item(sku): 
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0) 
    except Flavor.DoesNotExist:
        msg = 'We are out of {0}'.format(sku) 
        raise OutOfStock(msg)

# ObjectDoesNotExist
def list_any_line_item(model, sku):
    try:
        return model.objects.get(sku=sku, quantity__gt=0)
    except ObjectDoesNotExist:
        msg = 'We are out of {0}'.format(sku)
        raise OutOfStock(msg)
```

### 7.2.2 여러 개의 객체가 반환되었을 때

- `MultipleObjectsReturned` 예외처리. 예외를 발생시키거나 에러 로그를 남길 수 있음

```python
from flavors.models import Flavor
from store.exceptions import OutOfStock, CorruptedDatabase

def list_flavor_line_item(sku): 
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0) 
    except Flavor.DoesNotExist:
        msg = 'We are out of {}'.format(sku)
        raise OutOfStock(msg)
    except Flavor.MultipleObjectsReturned:
        msg = 'Multiple items have SKU {}. Please fix!'.format(sku) 
        raise CorruptedDatabase(msg)
```

## 7.3 쿼리를 좀 더 명확하게 하기 위해 지연 연산 이용하기

- 복잡한 쿼리의 경우 몇 줄 안되는 코드에 너무 많은 기능을 엮어서 기술하는 것을 피한다.

```python
# Don't do this!
from django.models import Q
from promos.models import Promo


def fun_function(name=None):
    """Find working ice cream promo"""
    # Too much query chaining makes code go off the screen or page. Not good.
    return Promo.objects.active().filter(Q(name__startswith=name)|Q(description__icontains=nam))

```

- 지연 연산(Lazy Evaluation)을 이용한다.
  - 지연 연산: 장고는 결과를 실행하기 전 까지는 실제로 SQL을 호출하지 않는 특징을 가짐
  - 따라서 여러줄에 나누어 써서 성능은 유지한 채 가독성은 향상시킬 수 있다. (주석도 더 쉽게 달 수 있음)

```python
# Do this!
from django.models import Q
from promos.models import Promo


def fun_function(name=None):
    """Find working ice cream promo"""
    results = Promo.objects.active()
    results = results.filter(
                Q(name__startswith=name) |
                Q(description__icontains=name)
            )
    results = results.exclude(status='melted')
    results = results.select_related('flavors')
    return results
```

### 7.3.1 Chaning!!!

```python
# Do this!
from django.models import Q
from promos.models import Promo


def fun_function(name=None): 
    """Find working ice cream promo"""
    qs = (Promo
             .objects
             .active()
             .filter(
                 Q(name__startswith=name) |
                 Q(description__icontains=name)
             )
             .exclude(status='melted')
             .select_related('flavors')
         )
    return qs

```

- Commenting out 할 때도 유용

```python
def fun_function(name=None): 
    """Find working ice cream promo"""
    qs = (Promo
             .objects
             .active()
            #  .filter(
            #      Q(name__startswith=name) |
            #      Q(description__icontains=name)
            #  )
             .exclude(status='melted')
             .select_related('flavors')
         )
    return qs
```

## 7.4 고급 쿼리 도구 이용하기

- 장고 ORM이 모든 경우를 완벽히 처리할 수 있는 것은 아님
- Python을 이용하여 데이터를 다듬을 수 있지만, 데이터 관리와 가공에서 데이터베이스가 월등히 빠름
- 고급 쿼리 도구를 이용하면 데이터베이스를 통해 데이터를 가공할 수 있음

### 7.4.1 쿼리 표현식

- [공식문서](https://docs.djangoproject.com/en/1.11/ref/models/expressions/)

- 먼저 아래 코드의 단점
  - 모든 고객 레코드에 대해서 Python for loop가 하나하나 돌고있다.
    - 매우 느리고, 메모리 소모가 큼
  - 경합상황 (race condition)
    - 여러 개의 프로세스가 공유 자원에 대해 동시에 접근을 시도하는 상태
    - 결과를 예측할 수 없음

    ```python
    # Don't do this!
    from models.customers import Customer


    customers = []
    for customer in Customer.objects.iterator():
        if customer.scoops_ordered > customer.store_visits: 
            customers.append(customer)
    ```

- 쿼리 표현식을 활용하여 수정
  - [F Expression 활용](https://docs.djangoproject.com/en/1.11/ref/models/expressions/#f-expressions)
  - [F Expression 활용하여 Race Condition 피하기](https://docs.djangoproject.com/en/1.11/ref/models/expressions/#avoiding-race-conditions-using-f)

    ```python
    from django.db.models import F
    
    from models.customers import Customer
    
    
    customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
    ```

    ```SQL
    SELECT * from customers_customer where scoops_ordered > store_visits
    ```

### 7.4.2 데이터베이스 함수들

- `UPPER()`, `LOWER()`, `COALESCE()`, `CONCAT()`, `LENGTH()`, `SUBSTR()`
- 장점
  - 쓰기 쉬움
  - 계산 Logic을 Python -> DB
  - 원래 DB마다 사용방식이 다르지만, Django ORM이 추상화 해주어서 신경쓰지 않아도 됨
- [공식문서](https://docs.djangoproject.com/en/1.11/ref/models/database-functions/)


## 7.5 필수 불가결한 상황이 아니라면 로우 SQL은 지양하자

- Django ORM은 높은 생산성을 제공
- 단순 쿼리 작성 뿐만 아니라 모델에 대한 접근, 업데이트 시 유효성 검사와 보안을 제공
- 로우 SQL 사용 시 이식성이 떨어질 수 있음 (DB 종류 고려)
- DB Migration시 불편 (DB 종류 고려)
- 월등히 간결해질 때는 사용

> 더 쉽다면 로우 SQL 사용하자, 단, extra는 자제하자... raw는 사용!

## 7.6 필요에 따라 인덱스를 이용하자

- `db_index=True`
- index를 지정하지 않고 시작하는 것을 추천
  - index가 빈번하게 사용되거나
  - indexing을 통해 성능 향상이 되는지 test 가능하면 index 추가
- PostgresSQL이라면, `pg_stat_activity`를 사용 가능
- Django 1.11에서는 `django.db.models.indexes`, `Index` Class, `Meta.indexes` 옵션 지원
- `django.contrib.postgres.indexes`는 현재 BrinIndex and GinIndex 지원

## 7.7 트랜잭션

- [참고하면 좋은 글](https://d2.naver.com/helloworld/407507)

### 7.7.1 각각의 HTTP 요청을 트랜잭션으로 처리하라

```python
# settings/base.py

DATABASE = {
  'default': {
    'ATOMIC_REQUESTS': True,
  }
}
```

- `ATOMIC_REQUESTS` 설정 : 모든 Request가 트랜잭션으로 처리
- `transaction.non_atomic_requests()` : 설정에서 제외하고 싶을 때

### 7.7.2 명시적인 트랜잭션 선언

- 어떤 뷰와 비지니스 로직이 하나로 엮여 있는지 명시해 주는 것
- 데이터베이스에 변경이 생기지 않는 작업은 트랜잭션 처리 X
- 데이터베이스에 변경이 생기는 작업은 트랜잭션 처리
- 대부분 ATOMIC_REQUESTS 설정으로 충분

### 7.7.3 django.http.StreamingHttpResponse와 트랜잭션

- `django.http.StreamingHttpResponse`를 Return하는 View는 중간에 트랜잭션 에러 처리 불가능
- 해결 방법
  - `ATOMIC_REQUESTS` -> False & 명시적 
  - 해당 뷰를 django.db.transaction.non_atomic_requests 데코레이터로 감싸기

### 7.7.4 MySQL에서의 트랜잭션

- 버전마다 트랜잭션 지원 여부가 다름 (InnoDB - 지원, MyISAM - 지원X)
- 트랜잭션을 지원하지 않는 경우, ATOMIC_REQUESTS의 설정이나 트랜잭션 설정 code에 관계없이 항상 autocommit mode로 작동

### 7.7.5 Django ORM 트랜잭션 자료

- [Django 공식 문서](docs.djangoproject.com/en/1.11/topics/db/transactions/)
- [Real Python (1.6)](https://realpython.com/transaction-management-with-django-1-6/)