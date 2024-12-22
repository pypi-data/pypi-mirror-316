from setuptools import setup, find_packages

setup(
    name='clockwise', # this is the package folder that contain the "main.py"
    version='1.0.3', # to increment this version number for each new version of this package
    packages=find_packages(), 
    install_requires=[ # dependencies for this package
    # e.g. 'numpy>=1.11.1'
    ],
)
