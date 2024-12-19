from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='csexamgenerator',
    version='2.0.1',
    description='An internal tool for exam submission',
    author='Obiwan',
    author_email='quan.do@coderschool.vn',
    packages=find_packages(),
    install_requires=[

    ],
    long_description=description,
    long_description_content_type='text/markdown',
)
