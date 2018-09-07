# 3. 어떻게 장고 프로젝트를 구성할 것인가

## 3.1 Django 1.11 프로젝트의 기본 구성

- `django-admin.py`로 project와 app 생성

    ```bash
    django-admin.py startproject mysite
    django-admin.py startapp my_app
    ```

	```
	# django-admin이 만들어주는 기본 django project tree

    mysite/
	   ├── manage.py
	   ├── my_app
	   │   ├── __init__.py
	   │   ├── admin.py
	   │   ├── apps.py
	   │   ├── migrations
	   │   │   └── __init__.py
	   │   ├── models.py
	   │   ├── tests.py
	   │   └── views.py
	   └── mysite
		   ├── __init__.py
		   ├── settings.py
		   ├── urls.py
		   └── wsgi.py
	```

## 3.2 ~~우리~~가 선호하는 프로젝트 구성

- django-admin startproject 명령어를 통해 생성된 project tree를 간략히 살펴보면 아래와 같다.

    ```
    <repository_root>/
    ├── <configuration_root>/
    ├── <django_project_root>/
    ```

### 3.2.1 Top-Level: Repository root

- project의 최상위 directory
- `README`, `manage.py`, `.gitignore`, `requirements.txt` 등의 파일들이 위치한다

### 3.2.2 Second-Level: Django project root

- Django project의 directory
- 설정 파일에 포함되지 않는 python code가 위치한다.

### 3.2.3 Second-Level: Configuration root

- `settings` module, 기준이 되는 `URL Conf` (urls.py) 등이 위치한다.
- django-admin.py startproject 명령어를 통해 생성하면, django project root 안에 위치한다. (repository root로 꺼내주는게 좋다.)

    ```
    # django-admin.py startproject 를 통해 생성된 project tree
    my_repo/  # <repository_root>
        └── mysite/  # <django_project_root>
            ├── manage.py
            ├── my_app/  # <django_app>
            │   ├── __init__.py
            │   ├── admin.py
            │   ├── apps.py
            │   ├── migrations
            │   │   └── __init__.py
            │   ├── models.py
            │   ├── tests.py
            │   └── views.py
            └── mysite/  # <configuration_root>
                ├── __init__.py
                ├── settings.py
                ├── urls.py
                └── wsgi.py
    ```
	
	```
    # configuration root directory를 옮긴 project tree
    my_repo/  # <repository_root>
        ├── manage.py
        ├── mysite/  # <configuration_root>
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        └── mysite/  # <django_project_root>
            └── my_app/  # <django_app>
                ├── __init__.py
                ├── admin.py
                ├── apps.py
                ├── migrations
                │   └── __init__.py
                ├── models.py
                ├── tests.py
                └── views.py
    ```
    
    > manage.py 위치가 변경되면서, (django\_proejct\_root -> repository\_root) startapp 명령어를 통해 app을 생성하면, django\_project\_root가 아닌, repository\_root에 django\_app이 생성된다.  
    >이러한 경우, manage.py startapp <app_name> <app_path>를 입력하면, 지정한 위치에 django\_app을 생성한다.  
    > [참고](https://stackoverflow.com/questions/33243661/startapp-with-manage-py-to-create-app-in-another-directory)
    

## 3.3 예제 프로젝트 구성

    ```
    icecreamratings_project  # <repository root>
    ├── config/  # <configuration root>
    │   ├── settings/
    │   ├── __init__.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── docs/  # 개발에 필요한 문서
    ├── icecreamratings/
    │   ├── media/  # 개발 환경에서 필요한 directory (사용자가 생성하는 파일의 root)
    │   ├── products/  # django_app
    │   ├── profiles/  # django_app
    │   ├── ratings/  # django_app
    │   ├── static/  # 사용자가 생성하지 않은, 정적 파일의 root (JS, CSS 및 image file)
    │   └── templates/  # Django template의 root
    ├── .gitignore
    ├── README.md
    ├── manage.py
    └── requirements.txt
    ```

> 큰 프로젝트에서는 `static/`과 `media/` directory 대신 static media server를 사용한다. (like AWS S3)


## 3.4 virtualenv

- 가상 환경의 위치는 project와 별도로 분리된 공간에 위치시키는게 좋다.
    
    ```
    # project는 proejct끼리, virtualenv는 virtualenv끼리
    
    ~/projects/icecreamratings_project/
    ~/.env/icecreamratings/
    ```


- 가상 환경 package들의 source code는 **절대** 편집하지 않는다.
    > package들의 버전은 오로지 `requirements.txt`에 종속성을 가진다.
    
## 3.5 startproject 살펴보기

- Django의 기본 startproject 대신 cookiecutter를 이용하면, 예제 프로젝트 구성처럼 fancy한 project layout을 기본적으로 구성해준다.
    
    [[Django Cookiecutter repo]](https://github.com/pydanny/cookiecutter-django)

