from setuptools import setup, find_packages

requirements = ['pytorch','torchvision','numpy','ultralytics', 'opencv']

setup(
    name='zebrafishBlood',
    version='0.1.9',
    description='Zebrafish blood smear cell counter',
    author=['Eunhye Yang'],
    author_email='eunhye@connect.hku.hk',
    packages=find_packages(),
    install_requires=requirements
)