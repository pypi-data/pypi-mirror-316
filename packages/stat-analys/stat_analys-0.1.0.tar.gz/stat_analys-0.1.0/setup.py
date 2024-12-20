# setup.py
from setuptools import setup, find_packages

setup(
    name='stat_analys',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'seaborn',
        'matplotlib',
        'plotly',
        'scipy',
        'sklearn',
        'tabulate',
        'dataclasses',
        'logging',
        'warnings',
        'collections'
    ],
    author='ADOGLI Jean-Paul',
    author_email='adoglijeanpaul@gmail.com',
    description='Un package pour l\'analyse statistique univariée',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Jean-Paul15/stat_analys',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
