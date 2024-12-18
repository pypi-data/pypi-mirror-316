import setuptools

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="mozartpy",  # Replace with your own username
    version='1.0.1rc0',
    # version="1.0.1.1",
    author="VMS Solutions",
    author_email="support@vms-solutions.com",
    description="Anaylize for Mozart Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.vms-solutions.com/en/",
    license="Ms-PL",
    packages=setuptools.find_packages(),# 서브패키지 명시적으로 표시해야함
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #setup_requires=['pythonnet>=2.5.2'],
    install_requires=['pythonnet>=2.5.2', 'zeep', 'tqdm', 'pandas', 'multipledispatch', 'matplotlib', 'py7zr', 'requests'],
    include_package_data=True,
    python_requires='>=3.6'
    # python_requires='>=3.6, <3.9'
)
# 1. package build command( *** 아래 명령어 실행되지 않을 때, pip install bdist_wheel 설치 *** )
# python setup.py sdist bdist_wheel
# 2. upload pypi ( *** 아래 명령어 실행되지 않을 때, pip install twine 설치 *** )
# twine upload dist/mozartpy-0.0.1-py3-none-any.whl
# 명령어 입력하면 자신의 username 과 password를 입력하라고 나오는데, 이때 pypi 에서 회원가입했던 username 과 password를 입력하면 된다.
# --> API Token 방식으로 변경됨, password는 ctrl+c, ctrl+v 가 아닌 드래그 우클릭 복사, cmd에서 우클릭>편집>붙여넣기 로 입력하여야 정상 입력됨
    # username: __token__
    # password: pypi-AgEIcHlwaS5vcmcCJDY1YTc4NmZjLTFlNGQtNGJlZi04ODE0LWE3NmU0ZWI5OWU0MwACKlszLCI0NDcwYTc4Zi0xOGEzLTRlMTMtYWUyNi1kYzQ4NmEwODliOWUiXQAABiBGCdNtD4O50UOpBv5gXMqIRVheNbZE8sU_oOABmGvRHw

# pip install --upgrade mozartpy (업그레이드 설치 명령어)

# test pypi : 2번에 올리기 전에 테스트용으로 사용
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/mozartpy-0.0.1-py3-none-any.whl
# python -m pip install --index-url https://test.pypi.org/simple/ --no-deps <mozartpy>
# test pypi 토큰
    # username: __token__
    # password: pypi-AgENdGVzdC5weXBpLm9yZwIkMDllYTMwMDgtZmRkOS00M2MxLWJmY2MtMzNhZDNlYjY1ZTNhAAIqWzMsImQ0OWU0OGE3LTM2NTYtNDUxYy1iYmRiLWNmNzc2MTQ4NmJlOSJdAAAGIEbNGvesSfGgV8lghtxAQU_M8Tn7_aZxqatTKwqC-g9R

# pypi 에 접속이 되지 않는 사이트를 위해 로컬에서 설치할 수 있도록 의존성을 포함해서 dowload 한 후에 배포하여
# 사용할 때( 참고사이트, https://kmdigit.github.io/2020/05/08/python-install-pip-offline/)
# 1. pypi 에서 의존성 패키지를 포함하여 모두 다운로드( 아래 명령어 사용)
#    pip download -d . mozartpy
# 2. 로컬경로의 패키지 설치 : 전달 받은 패키지 파일을 압축해제하여 해당 경로로 이동후 다음의 명령어로 설치
#    pip install --no-index -f . mozartpy ( .은 현재 디렉토리를 의미함)
#