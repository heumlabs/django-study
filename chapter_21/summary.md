# 21. Django’s Secret Sauce: Third-Party Packages

- 오픈소스 커뮤니티에서 제공되는 서드파티 파이썬/장고 패키지가 장고의 진정한 강점
- 전문적인 파이썬/장고 개발은 서드파티 패키지를 프로젝트에 통합하는 일. 모든 도구를 처음부터 만들기는 힘들 것.

## 21.1 서드파티 패키지의 예시

- 교재의 Appendix A 참고
  - *같이 훑어보기!*
- [Awesome Python](https://github.com/vinta/awesome-python)
- [Awesome Django](https://github.com/vinta/awesome-python)

## 21.2 PyPI (Python Package Index)

- [Link](https://pypi.python.org/pypi)
- 파이썬 패키지 저장소
- 현재 ****개의 패키지가 저장되어 있음
- [pip](https://pypi.org/project/pip/)로 PyPI의 (다운로드 가능한) 패키지를 다운로드/설치함
- [PyConKr 2018 "나도 할 수 있다 오픈소스"](https://www.slideshare.net/kanghyojun/ss-110767619)

## 21.3 DjangoPackages.org

- [link](https://djangopackages.org/)
- 장고프로젝트를 위한 재사용 가능한 앱, 사이트, 도구 등을 모아놓은 사이트
- PyPI처럼 패키지를 저장해놓은 곳은 아님. PyPI, Github등으로 부터 수집한 데이터/지표를 보여주는 곳. (사용자가 입력한 정보 포함)
- 패키지들을 비교해보기 좋음

> hard metrics?, soft data?, Jannis Gebaueur?

## 21.4 다양한 패키지를 알아두자

- 바퀴를 재발명하지 말고 서드파티 패키지를 알아보자. 거인들의 어깨 위에 서자. 좋은 라이브러리들이 전 세계의 개발자들에 의해 잘 작성되고, 문서회되고, 테스트됨.
- 그 패키지를 이용하면서 코드를 공부할 수 있음 (패턴 등)
- 좋은 패키지와 나쁜 패키지를 구별할 수 있어야 함 (섹션 21.10)

## 21.5 패키지 설치, 관리를 위한 도구들

- virtualenv & pip
- [스포카 홍민희 "파이썬의 개발 환경(env) 도구들"](https://spoqa.github.io/2017/10/06/python-env-managers.html)

## 21.6 패키지 요구사항

- `requirements` 폴더 내의 requirements 파일로 관리
- 챕러 5에서 다룸

## 21.7 장고 패키지 이용하기: 기본

서드파티 패키지를 찾을 때는 아래 단계를 따르도록 한다.

### 1단계 : 패키지 문서 읽기

:smile:

### 2단계 : 패키지와 버전을 requirements에 추가하기

- ex) `Django==1.11`
- 반드시 버전을 명시함. Stable!

### 3단계 : virtualenv에 requirements 설치

:smile:

### 4단계 : 패키지의 설치 문서를 그대로 따라하기

- Don'tskip

## 21.8 서드파티 패키지에 문제가 생겼을 때

- 패키지 저장소의 이슈 트래커 확인. 보고되지 않은 버그라면 보고하기.
-  StackOverflow, IRC #django 활용

## 21.9 자신의 장고 패키지 릴리스 하기

- 장고 공식 문서 "Django’s Advanced Tutorial: How to Write Reusable Apps" [Link](https://docs.djangoproject.com/en/1.11/intro/reusable-apps/)
- 추가로 추천하는 작업
  - 공개 저장소 생성 (Github)
  - PyPI에 패키지 올리기 ([참고 Link](https://packaging.python.org/distributing/#uploading-your-project-to-pypi))
  - [djangopackages.org]()에 추가
  - [Read the Docs](https://readthedocs.io/)를 활용하여 Sphinx 문서 호스팅

## 21.10 좋은 장고 패키지의 요건

새로운 Django 패키지를 만들 때 사용할 수 있는 페크리스트

### 21.10.1 목적

- 패키지 이름이 목적을 잘 설명해야 함
- django 관련 패키지는 'django-' 또는 'dj-'를 붙여야 함

### 21.10.2 범위

- 한 가지 작은 일에 집중
- 사용자가 패키지를 쉽게 패치하거나 교체할 수 있어야 함

### 21.10.3 문서화

- 23장 참고
- 필수
- ReStructuredText로 문서 작성
- Sphinx, public 호스팅
- readthedocs.io

### 21.10.4 테스트

- 필수
- 더 나은 품질의 PR을 얻을 수 있다

### 21.10.5 양식

- 기본 template 제공 (like Django)
- css는 제외된 상태

### 21.10.6 활동

- 정기적 업데이트 필요
- repo에서 코드를 업데이트되면 PyPI에 릴리스 해야함

### 21.10.7 커뮤니티

- 모든 기여자는 CONTRIBUTOR.rst 또는 AUTHORS.rst 파일에 표시
- 다른 개발자의 포크 관리

### 21.10.8 모듈성

- django 패키시에 쉽게 플러그인 가능해야함
- 프로젝트에 최소한으로 관여하도록 함

### 21.10.9 PyPI

- 반드시 PyPI에 올린다
- 사용자가 업데이트 받기 쉬움

### 21.10.10 가능한 넓은 범위의 requirements 작성

```
# DON'T DO THIS!
# requirements for django-blarg
Django==1.10.2
requests==1.2.3
```

```
# requirements for django-blarg
Django>=1.10,<1.12
requests>=2.6.0,<=2.13.0
```

### 21.10.11 적절한 버전 명

- `A.B.C` 패턴
  - A : Major. 대규모 변경 등
  - B : Minor. Deprecation Notice 등
  - C : Bugfix. Micro Release라고도 함
- `alpha`, `beta`, `release-candidate(rc)` 접미사는 버전 뒤에 명시
  - `Django 1.11-alpha`, `django-crispy-forms 1.6.1-beta`
- 제발 완성되지 않은 코드를 PyPI에 업로드하지 마라
- [PEP 386](https://www.python.org/dev/peps/pep-0386/)
- [Sementic Versioning](https://semver.org/)

### 21.10.12 이름

- 이미 PyPI에 등록되어있지 않은지 확인
- Django Package에 없는지 확인
- 너무 이상한 이름은 사용하지 말자

### 21.10.13 라이센스

- 반드시 필요 (TIP 필독)
- `LICENSE.rst` 작성

### 21.10.14 코드의 명확성

- 코드는 가능한 한 명확하고 단순하게

### 21.10.15 URL Namespaces 이용

- 섹션 8.4
- URL Namespace를 사용해서 프로젝트 간 충돌을 방지

## 21.11 쉬운 방법으로 패키지 만들기

- [Cookie Cutter for Python Package](https://github.com/audreyr/cookiecutter-pypackage)
- [Cookie Cutter for Django Package](https://github.com/pydanny/cookiecutter-djangopackage)

## 21.12 오픈소스 패키지 관리하기

### 21.12.1 PR(Pull Request)에 대한 보상

- 누군가의 PR을 수락했다면 `CONTRIBUTORS.txt`나 `AUTHORS.txt`에 기록
- [Django AUTHORS](https://github.com/django/django/blob/master/AUTHORS)

### 21.12.2 나쁜 PR 다루기

- Test 실패
- Test Coverage 넘어감
- PR의 변경 내용은 최대한 작게
- (너무) 복잡한 코드
- PEP8을 지키지 않은 코드
- 공백 처리와 섞여있는 코드 변경 건

### 21.12.3 PyPI에 정식으로 릴리스하기

- 프로젝트 저장소는 품질이 보장된 곳이 아님. PyPI에 공식적으로 업로드해서 배포.
- Twine : PyPI 업로드 시 사용되는 라이브러리
- [나도 할 수 있다 오픈소스 - PyCon2018](https://www.slideshare.net/kanghyojun/ss-110767619)

### 21.12.4 PyPI에 배포할 때 Wheel 활용

- [PEP 427](https://www.python.org/dev/peps/pep-0427/)에 따르면 Wheel은 새로운 파이썬 패키지 배포 표준
- egg 대체
- 빠른 설치, 보안
- pip >= 1.4, setuptools >= 0.8 부터

### 21.12.5 새 버전의 Django로 업그레이드 하라

- Django의 최신 버전에서 테스트 해보아야 함

### 21.12.6 좋은 보안 예시 프로젝트들을 따르라

- 챕터 26 참고
- [더 좋은 링크](https://alexgaynor.net/2013/oct/19/security-process-open-source-projects/)
  - *"보안 취약성으로 인해 사용자가 위험에 노출될 수 있다. 소프트웨어의 제작자이자 배포자인 사용자는 악용되는 것을 피할 수 있는 방법으로 보안 릴리스를 처리할 책임이 있습니다."*

### 21.12.7 기본 예제 템플릿을 제공하라

- 예제 템플릿을 제공하여 쉽게 테스트해볼 수 있도록 해야 함
- [cookie cutter 예시](https://github.com/pydanny/cookiecutter-djangopackage/blob/master/%7B%7Bcookiecutter.repo_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/templates/%7B%7Bcookiecutter.app_name%7D%7D/base.html)

### 21.12.8 Package 넘겨주기

- 관리가 힘들다면 활동적인 메인테이너에게 패키지 관리권을 넘겨주기
- 사례
  - Ian Bicking의 "pip/virtualenv"
  - Daniel & Audrey Roy Greenfeld의 "djangopackages.org"
  - Daniel Roy Greenfeld의 "django-uni-form", "dj-stripe"
  - Rob Hudson의 "django-debug-toolbar"

## 21.13 더 읽어볼 것

- http://djangoappschecklist.com/
- http://alexgaynor.net/2013/sep/26/effective-code-review/
- https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
- https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/