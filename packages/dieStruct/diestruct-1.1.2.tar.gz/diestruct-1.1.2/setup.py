# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dieStruct',
    version='1.1.2',
    description='Librería para comprender el analísis y diseño estructural',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Daniel Ilbay Yupa',
    author_email='daningenio@gmail.com',
    url='https://www.youtube.com/results?search_query=daningenio',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],  

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Education',
    ],
                      

)