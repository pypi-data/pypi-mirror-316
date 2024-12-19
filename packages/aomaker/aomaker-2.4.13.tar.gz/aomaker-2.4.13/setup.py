# --coding:utf-8--
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="aomaker",
    version="2.4.13",
    author="ancientone",
    author_email="listeningsss@163.com",
    description="An api testing framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ae86sen/aomaker",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'black==23.11.0',
        'Jinja2==3.1.2',
        'jsonpath==0.82',
        'loguru==0.6.0',
        'PyMySQL',
        'pytest==7.2.0',
        'PyYAML==6.0',
        'requests==2.28.1',
        'allure-pytest==2.8.24',
        'pydantic==1.10.2',
        'mitmproxy==9.0.1',
        'colorlog==6.7.0',
        'jsonschema==4.17.3',
        'genson==1.2.2',
        'click==8.1.3',
        'emoji==2.2.0',
        'click-help-colors==0.9.1',
        'tenacity==8.2.3',
        'ruamel.yaml==0.17.21',
        'tabulate==0.9.0',
        # 'fastapi==0.110.0',
        # 'uvicorn==0.28.0'

    ],
    entry_points={
        'console_scripts': [
            'amake=aomaker.cli:main_make_alias',
            'arun=aomaker.cli:main_arun_alias',
            'arec=aomaker.cli:main_record_alias',
            'aomaker=aomaker.cli:main',
        ]
    }
)