from setuptools import setup, find_packages

requirements = [
    'scikit-build','torch','torchvision','numpy',
    'ultralytics','opencv-python','openslide-python',
    'openslide-bin','joblib'
]

setup(
    name='zebrafishBlood',
    version='0.2.5',
    description='Zebrafish blood smear cell counter',
    long_description='For python>=3.8',
    author=['Eunhye Yang'],
    author_email='eunhye@connect.hku.hk',
    packages=find_packages(),
    install_requires=requirements
)