from setuptools import setup, find_packages

setup(
    name='fatigue_calculator',
    version='0.1.0',
    description='A scientifically-grounded cognitive fatigue prediction system.',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'openpyxl>=3.1',
        'pytest',
        'numpy',
    ],
    extras_require={
        'dev': ['pytest'],
    },
    python_requires='>=3.7',
) 