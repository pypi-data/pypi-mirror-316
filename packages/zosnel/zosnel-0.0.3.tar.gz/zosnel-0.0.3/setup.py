# setup.py

from setuptools import setup, find_packages

setup(
    name="zosnel",
    version="0.0.3",
    description="A python framework for simple web apps.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="SachchitMishra",
    author_email="sachchitroymishra@hotmail.com",
    url="https://github.com/Zosnel/Zosnel",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
