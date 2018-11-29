# 23. 문서화에 집착하라

## 23.1 Python 문서를 reStructuredText로 작성하기

reStructuredText(이하 RST)는 Python 프로젝트를 문서화하는 데 사용되는 가장 일반적인 Markup 언어다.

다음은 RST의 사양과 이를 사용하는 데 도움이 되는 몇 가지 샘플 프로젝트의 링크다.

- [[RST docs]](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html)
- [[Django docs]](https://docs.djangoproject.com/en/1.11/)
- [[Python docs]](https://docs.python.org)

간단한 기본 명령어들

```
Section Header
==============

**emphasis (bold/strong)**

*italics*

Simple link: https://twoscoopspress.com

Fancier Link: `Two Scoops of Django`_
.. _Two Scoops of Django: https://twoscoopspress.com

Subsection Header
-----------------

#) An enumerated list item

#) Second item

* First bullet

* Second bullet

* Indented Bullet

* Note carriage return and indents

Literal code block::

    def like():
        print("I like Ice Cream")

    for i in range(10):
        like()

Python colored code block (requires pygments):

   code-block:: python

    # You need to "pip install pygments" to make this work.
       
   for i in range(10):
       like()

JavaScript colored code block:

   code-block:: javascript

       console.log("Don't use alert()")
```

## 23.2 Sphinx를 사용하여 RST 문서 만들기

[[Sphinx docs]](http://www.sphinx-doc.org/en/stable/)

## 23.3 Django Project에는 어떤 문서가 있어야 하는가?

- README.rst
- docs/
- docs/deployment.rst
- docs/installation.rst
- docs/architecture.rst

## 23.4 추가 문서 리소스

- [[PEP 0257]](https://python.org/dev/peps/pep-0257): Docstring 관련
- [[Read The Docs]](https://readthedocs.io): 무료 Sphinx 호스팅 서비스
- [[PythonHosted]](https://pythonhosted.org): 무료 도큐먼트 호스팅 서비스


## 23.5 MarkDown

MarkDown은 RST와 크게 다르지 않은 text reformating syntax다.

오픈소스에 RST 대신 MarkDown을 사용하는 경우 다음을 유의:

- RST를 제외한 다른 형식은 PyPI에서 long\_description을 format하지 않는다.
- 많은 Python, Django 개발자는 MarkDown보다 RST 기반 문서를 많이 검색한다.

### 23.5.1 README.md to README.rst: PyPI에 업로드된 패키지에 Pandoc 사용하기

```python
import subprocess
import sys

if sys.argv[-1] == 'md2rst':
    subprocess.call('pandoc README.md -o README.rst', shell=True)
```

Pandoc은 파일을 한 마크업 형식에서 다른 형식으로 변환할 수 있는 command line tool이다.

[[subprocess??]](https://www.pythonforbeginners.com/os/subprocess-for-system-administrators)

### 23.5.2 MarkDown 리소스

- [[wiki - MarkDown]](https://en.wikipedia.org/wiki/Markdown)
- [[mkdocs.org]](http://mkdocs.org)
- [[documentup.com]](http://documentup.com)
- [[progrium.viewdocs.io]](http://progrium.viewdocs.io)
- [[pandoc]](https://johnmacfarlane.net/pandoc)

## 23.6 Wiki 및 기타 문서 작성법

어떤 이유로든 프로젝트 자체에 개발자를 위한 문서를 배치할 수 없는 경우 다른 옵션이 있어야 한다. Wiki나 온라인 문서 저장소 및 워드프로세스 문서는 버전 관리 기능을 가지고 있지 않지만, 문서화를 하지 않는 것보다는 낫다.

이전 표에서 제시된 것과 동일한 이름의 문서를 다른 방식으로 작성하는 것을 고려하라.

## 23.7 요약

- RST를 사용하여 Plain text format의 문서 작성
- Sphinx를 사용하여 문서를 HTML과 EPUB format으로 렌더링. LaTeX 설치 방법을 알고 있다면 PDF로도 렌더링 가능
- Django 프로젝트에 대한 문서화 요구사항
- MarkDown을 이용하여 문서를 작성하고, RST로 변환하는 법

