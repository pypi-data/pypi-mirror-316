# setup.py

from setuptools import setup, find_packages

setup(
    name='graylog_telemidia',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'graypy',
    ],
    description='Uma abstração da biblioteca graypy, projetada para adaptar as requisições do Graylog ao padrão utilizado pela Telemidia.',
    author='Thales Casa Grande de Lima',
    author_email='thales.lima@telemidia.net.br',
    url='http://git.telemidia.net.br/Telemidia/graylog-telemidia-py',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)