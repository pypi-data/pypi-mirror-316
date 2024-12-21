from setuptools import setup, find_packages

setup(
    name='android_notify',
    version='0.1',
    description='A Python package for sending Android notifications.',
    packages=find_packages(),
    install_requires=['pyjnius'],
)
