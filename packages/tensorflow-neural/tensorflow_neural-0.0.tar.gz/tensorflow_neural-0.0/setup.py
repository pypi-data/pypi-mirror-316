from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() #Gets the long description from Readme file

setup(
    name='tensorflow_neural',
    version='0.0',
    packages=find_packages(),

    author='nndl',
    author_email='nndl@xyz.com',
    description='This is the short description',

    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',

)