# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='manc',
    version='0.1.0',
    description='一款可以接入自定义扩展的爬虫',
    url='https://github.com/markadc/cman',
    author='WangTuo',
    author_email='markadc@126.com',
    packages=find_packages(),
    license='MIT',
    zip_safe=False,
    install_requires=['requests', 'parsel'],
    keywords=['Python', 'Spider'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
