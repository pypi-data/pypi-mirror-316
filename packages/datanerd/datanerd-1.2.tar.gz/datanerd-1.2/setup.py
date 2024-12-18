from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2'
DESCRIPTION = 'Contains multiple functions stats(), iv_woe(), pushdb(), teams_webhook(), and ntfy()'


# Setting up
setup(
    name="datanerd",
    version=VERSION,
    author="Sunil Aleti",
    author_email="iam@sunilaleti.dev",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'sqlalchemy', 'pyodbc', 'requests'],
    keywords=['python', 'describe', 'stats', 'unique values', 'information value', 'woe','iv'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)