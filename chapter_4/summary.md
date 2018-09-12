# 4. 장고 앱 디자인의 기본

- Django Project
- Django App
- INSTALLED_APPS
- 3rd-party Django Packages

## 4.1 장고 앱 디자인의 황금률

> "Write programs that do one thing and do it well." - [James Bennett](https://www.b-list.org/)
> "한 가지일을 하고, 한 가지 일을 잘하는 프로그램을 짜라" - 제임스 베넷

- [유닉스 철학](https://ko.wikipedia.org/wiki/%EC%9C%A0%EB%8B%89%EC%8A%A4_%EC%B2%A0%ED%95%99)
- 각 앱이 주어진 임무에만 집중할 수 있어야 함
  - 앱을 설명할 때 "그리고", "또한"이란 단어를 한 번 이상 사용한다면, 앱을 나눌 때가 된 것!

## 4.2 장고 앱 네이밍

- **한 단어**
  - flavors, animals, blog, polls
- **복수형** : 앱의 메인 모델 이름의 복수형
  - 의미가 적절할 때만. (ex. blog)
- **URL** 고려
  - `http://www.example.com/weblog/`를 원한다면 메인 모델이 `Post`라도 App 이름은 `weblog`가 적절할 수 있다.
- **PEP8**에 맞게 `import`될 수 있는 이름
  - 숫자, 특수 기호(`-`, `,`, `.`) 없이
  - 가독성을 위해 밑줄 이용

## 4.3 Keep Apps Small

> Keep Apps Small, Stupid!

- App은 언제든 쪼개고 다시 작성할 수 있다고 생각
  - *너무 완벽하게 하려고 무리하지마라.*
- App은 가능한 작게 유지

## 4.4 앱 안에는 어떤 모듈이 있는가?

### 4.4.1 공통 앱 모듈

```bash
# Common modules
scoops/
├── __init__.py
├── admin.py
├── forms.py
├── management/
├── migrations/
├── models.py
├── templatetags/
├── tests/
├── urls.py
├── views.py
```

### 4.4.2 비공통 앱 모듈

```bash
# uncommon modules
scoops/
├── api/
├── behaviors.py
├── constants.py
├── context_processors.py
├── decorators.py
├── db/
├── exceptions.py
├── fields.py
├── factories.py
├── helpers.py
├── managers.py
├── middleware.py
├── signals.py
├── utils.py
├── viewmixins.py
```

- `api` 패키지
  - api를 생성할 때 필요한 다양한 모듈을 격리하기 위해 만든 패키지
- `behaviors.py`
  - Model Mixins
- `constants.py`
  - App-level 세팅 값
- `decorators.py`
- `db` 패키지
  - Custom model fields 혹은 components
- `fields.py`
  - 보통 Form Field. 가끔 Model Field
- `factories.py`
  - Where we like to place our test data factories.
- `helpers.py`
  - Helper 함수
  - utils.py와 동일
- `managers.py`
  - Model이 너무 커지면 Custom Model Manager는 이 모듈로 이동
- `signals.py`
  - Custom signals
- `utils.py`
  - helpers.py와 동일
- `viewmixins.py`
