from setuptools import setup, find_packages

setup(
    name='neszen_helper',
    version='0.3.0',
    description='A simple package to convert text to uppercase and lowercase',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[

    ], 
)