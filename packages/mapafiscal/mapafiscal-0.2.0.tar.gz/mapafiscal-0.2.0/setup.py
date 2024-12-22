# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools import setup
from setuptools import find_packages

from mapafiscal import __version__
    
def parse_requirements(filename):
    with open(filename, encoding='utf-16') as f:
        return f.read().splitlines()

setup(name='mapafiscal',
    version=__version__,
    license='MIT',
    author='Ismael Nascimento',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author_email='ismaelnjr@icloud.com',
    keywords='mapa fiscal tributario receita federal',
    description=u'Gerador de mapa fiscal com base em regras fiscais',
    url='https://github.com/ismaelnjr/mapafiscal-project.git',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


