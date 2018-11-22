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

## 21.10

(다음번 스터디 때 진행)