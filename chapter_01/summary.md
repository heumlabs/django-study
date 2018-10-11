# 1. 코딩 스타일

## 1.1 읽기 쉬운 코드의 중요성 PEP20

- 변수명을 축약해서 쓰지 말자
- Function Argument의 이름은 반드시 쓰자
- Class와 Method는 문서화하기
- 주석 달기
- 재사용 가능한 코드는 리팩터링 해두자
	- (재사용 가능한 fuction이나 method로)
- Function이나 Method는 작은 Size를 유지하자
	- 스크롤이 필요없는 길이로!

예시)
`balance_sheet_decrease`
`bsd` or `bal_s_d`

## 1.2 PEP8

- [Python 공식 스타일 가이드](python.org/dev/peps/pep-0008/ )
- 사용하는 Editor에 PEP8을 준수하는지 Check해주는 Plugin 깔도록 하자
	- [Flake8](http://flake8.pycqa.org/en/latest/user/configuration.html)
- 기존 프로젝트는 기존의 Convention을 따르도록 하자
	- [A Foolish Consistency is the Hobgoblin of Little Minds](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds)
- [1줄의 글자 수 제한](https://www.python.org/dev/peps/pep-0008/#maximum-line-length)
	- Open Source Project : 79자
	- Private Project : 99자로 완화해서 사용해도 OK

## 1.3 Import 관련
- 아래 순서로 Import 문을 작성한다.
	1. **Standard library** imports. 
	2. Imports from **core Django** 
	3. Imports from **third-party apps** including those unrelated to Django. 
	4. Imports from **the apps that you created** as part of your Django project 

## 1.4 Explicit Relative Imports 사용

- Absolute Import 
	- **현재 app 외부**에서 사용
- Explicit Relative Import
	- **현재 app 내부**에서 다른 module을 import할 때 사용
- Implicit Relative Import
	- 권장하지 않음. (보통 **현재 app 내부**에서 다른 module을 import할 때 사용)

Django app의 이름을 바꾼다던가, 재사용 시 이름이 충돌하는 경우를 막을 수 있음

```
TIP: Doesn’t PEP 328 Clash With PEP 8? 
® python.org/pipermail/python-dev/2010-October/104476.html 
Additional reading: python.org/dev/peps/pep-0328/ 
```

## 1.5 Import * 피하기

- 명시적으로 모듈을  지정하여 Import 한다.
- 현재 Module 혹은 이전에 Import된 Module의 Namespace를 덮어쓸 수 있다.

## 1.6 Django 코딩 스타일

- [공식 문서 참고](docs.djangoproject.com/en/1.11/internals/contributing/writing-code/coding-style/ )
- URL Pattern Name에는 Dash(`-`) 보다는 Underscore(`_`)를 사용한다.
- Template Block Name에도 Dash(`-`) 보다는 Underscore(`_`)를 사용한다.

## 1.7 JS, HTML, CSS 스타일 선택하기

- JS : [ESLint](eslint.org)
- HTML & CSS : [Stylelint](stylelint.io)

## 1.8 IDE(혹은 Text Editor)에 종속되는 코딩은 하지 않기

- 예시) Template Tag 찾기 힘듦. <app_name>_tags.py 등의 Naming Pattern을 따른다.
