# 20. 장고의 사용자 모델 다루기

## 20.1 장고 도구를 이용하여 사용자 모델 찾아보기

```bash
# 기본 사용자 모델의 정의
>>> from django.contrib.auth import get_user_model
>>> get_user_model()
<class 'django.contrib.auth.models.User'>

# 프로젝트에 커스텀 사용자 모델 정의를 이용할 때
>>> from django.contrib.auth import get_user_model
>>> get_user_model()
<class 'profiles.models.UserProfile'>
```

프로젝트 설정에 따라 각기 다른 두 개의 User 모델이 존재할 수도 있다.  
하지만 이는 프로젝트가 두 개의 다른 User 모델을 가질 수 있다는 의미는 아니다.

### 20.1.1 사용자의 외래 키에 settings.AUTH_USER_MODEL을 이용하기

Django 1.11에서 공식적으로 User를 ForeignKey나 OneToOneField 또는 ManyToManyField에 붙이는 방법은 다음과 같다.

```python
from django.conf import settings
from django.db import models


class IceCreamStore(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255)
```

### 20.1.2 사용자의 외래 키에 get_user_model()을 쓰지 말자

이는 import loop를 만들 수 있는 위험한 방법이다.

```python
from django.contrib.auth import get_user_model
from django.db import models


class IceCreamStore(models.Model):

    # 아래 줄의 코드는 import loop를 만들 수 있다
    owner = models.OneToOneField(get_user_model())
    title = models.CharField(max_length=255)
```

## 20.2 장고 1.11 프로젝트를 위한 커스텀 유저 필드

> django-authtools는 커스텀 사용자 모델을 쉽게 정의할 수 있는 라이브러리다.  
> 특히 [AbstactEmailUser](https://github.com/fusionbox/django-authtools/blob/master/authtools/models.py#L27)와 [AbstractNamedUser](https://github.com/fusionbox/django-authtools/blob/master/authtools/models.py#L59) 모델이 많이 사용된다.  

[[django-authtools doc]](https://django-authtools.readthedocs.org/)  
[[django-authtools repo]](https://github.com/fusionbox/django-authtools)

### 20.2.1 Option 1: Subclass AbstractUser

장고의 사용자 모델 필드를 있는 그대로 사용하면서 추가 필드가 필요한 경우, 이 옵션을 선택한다.  

```python
# profiles/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class KarmaUser(AbstractUser):
    karma = models.PositiveIntegerField(verbose_name='karma',
                                        defaul=0,
                                        blank=True)
```

아래의 내용을 settings에 추가한다.

```python
AUTH_USER_MODEL = 'profiles.KarmaUser'
```

### 20.2.2 Option 2: Subclass AbstractBaseUser

AbstractBaseUser는 password, last\_login, is\_active 3개의 필드를 가진 최소한의 모델이다.

아래의 경우에 이 옵션을 선택:

- first\_name, last\_name과 같은 기본적으로 제공되는 필드가 마음에 들지 않는 경우
- 극도로 순수한 상태로 시작하는 것을 좋아하면서, 비밀번호 저장방식의 이점을 취하고 싶은 경우

[[Official Django Documentation Example]](https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#a-full-example)  
[[Source code of django-authtools]](https://github.com/fusionbox/django-authtools)

## 20.2.3 Linking Back From a Related Model

이 코드는 장고 1.5 이전의 프로젝트에서 사용하던 `Profile` 모델을 만드는 테크닉과 매우 유사하다.  
이 방식을 폐기하기 전에 다음 사용사례를 고려하라.

##### 사용사례: 3rd-party package 생성

- PyPI에 게시하기 위해 패키지를 만드는 경우
- 사용자당 추가정보(e.g. Stripe ID 또는 지불 gateway identifier)를 저장해야 하는 경우
- 기존 프로젝트 코드에 최대한 쉽게 접근하기를 원하는 경우

##### 사용사례: 내부 프로젝트 요구사항

- 자체 장고 프로젝트에서 일하는 경우
- 다양한 유형의 사용자가 서로 다른 필드를 사용하기 원하는 경우
- 특정 사용자들은 다른 사용자 유형의 조합으로 이루어진 경우
- 해당 문제를 모델 수준에서 처리하고자 하는 경우
- 1번 또는 2번 옵션의 커스텀 사용자 모델과 함께 이 모델을 사용하기를 원하는 경우


```python
# profiles/models.py
from django.conf import settings from django.db import models
from flavors.models import Flavor


class EaterProfile(models.Model):
    # Default user profile
    # If you do this you need to either have a post_save signal or
    #     redirect to a profile_edit view on initial login.
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    favorite_ice_cream = models.ForeignKey(Flavor, null=True, blank=True)

class ScooperProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    scoops_scooped = models.IntegerField(default=0)
    

class InventorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    flavors_invented = models.ManyToManyField(Flavor, null=True, blank=True)
```

> 3rd-party 라이브러리의 명시적인 목적이 프로젝트 커스텀 사용자 모델을 정의하는 것(django-authtools과 같이)이 아니라면, 3rd-party 라이브러리는 옵션 1 또는 2를 사용하여 사용자 모델에 필드를 추가하면 안된다. 대신 옵션 3에 의존해야한다.

## 20.3 요약

이 장에서는 사용자 모델을 찾고, 커스텀 사용자 모델을 정의하는 새로운 방법을 다루었다.

프로젝트의 필요에 따라 현재의 작업 방식을 계속 사용하거나, 실제 사용자 모델을 커스터마이즈 할 수 있다.
