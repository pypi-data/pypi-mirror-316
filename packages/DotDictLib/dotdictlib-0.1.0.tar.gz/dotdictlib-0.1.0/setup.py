from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name="DotDictLib",
    version="0.1.0",
    description="A class for dot notation access to dictionaries",
    author="Adarsh Dhiman",
    author_email="adarshdhiman007@gmail.com",
    packages=["dictator"],  # Optional, specify the directory if it's inside a package
    ext_modules=cythonize([
        Extension(
            'dictator.dot_dict',  # This matches the file name of dot_dict.pyx
            sources=['dictator/dot_dict.pyx'],
        )
    ]),
)
