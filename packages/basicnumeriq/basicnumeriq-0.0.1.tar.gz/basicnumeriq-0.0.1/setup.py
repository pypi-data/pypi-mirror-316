from setuptools import setup, find_packages

setup(
    name="basicnumeriq",
    version="0.0.1",
    description="A simple math operations library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="furkankarakuz",
    url="https://github.com/furkankarakuz/basicnumeriq",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10")
