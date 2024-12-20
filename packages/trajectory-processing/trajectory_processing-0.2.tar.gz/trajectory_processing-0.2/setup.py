# setup.py

from setuptools import setup, find_packages

setup(
    name="trajectory_processing",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'geopandas',
        'ptrail',
        'numpy',
        'scipy',
        'matplotlib',
        'joblib',
        'scikit-learn',
        'torch',
    ],
    author="Name",
    author_email="email@example.com",
    description="A package for processing trajectory data",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
