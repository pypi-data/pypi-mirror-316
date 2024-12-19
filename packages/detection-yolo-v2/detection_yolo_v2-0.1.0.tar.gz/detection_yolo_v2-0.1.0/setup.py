from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.1.0'

setup(
    name='detection-yolo-v2',
    version=VERSION,
    packages=find_packages(),
    python_requires='>3.8',
)