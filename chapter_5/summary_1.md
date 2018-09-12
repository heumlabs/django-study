# Settings와 Requirements 파일 (1)

> 5.1, 5.2, 5.3 요약

- Django 1.11은 settings 모듈에서 150가지가 넘는 setting을 조정할 수 있음
- Setting 값은 서버가 시작할 때 로드되며, 서버 재시작 말고는 운영 중일때 setting을 바꾸지 않는다.
- 주요 Tip
  - 모든 Setting 값은 버전 관리가 되어야 함
  - 반복되는 내용은 Base Setting에서 상속 (복붙금지)
  - Secret Key들은 VCS에서 제외

## 5.1 버전 관리되지 않는 Local Settings은 피한다.

- `SECRET_KEY`, `아마존 API 키` 등을 저장소에서 제외해야 함

- 버전 관리되지 않는 Local Settings 파일이 존재할 시 문제점
  - 모든 Machine에 Untracked Code 존재
  - Local에서 Production 환경의 버그 재현 불가
  - local_settings를 모두가 복사/붙여넣기 해야함 (`Dont Repeat Tourself`)

- 환경 별 Settings 파일을 공통된 객체에서 상속받아 VCS에서 관리해야 함

## 5.2 여러 개의 Settings 파일 사용하기

```bash
settings/
├── __init__.py
├── base.py
├── local.py
├── staging.py
├── test.py
├── production.py
├── ci.py
```

- *Each settings module should have its own corresponding requirements file*
- `--settings=twoscoops.settings.lo
- 유일하게 import * 구문을 이용해도 됨
- 개발자 별 세팅 파일 : `local_audreyr.py`
