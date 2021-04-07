from setuptools import find_packages, setup


def long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        desc = f.read()
    return desc

def install_requires():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requires = f.read().split("\n")
    return requires


setup(
    name="SRTrain",
    author="ryanking13",
    author_email="def6488@gmail.com",
    version="2.0.1",
    description="SRT(Super Rapid Train) wrapper for python",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/ryanking13/SRT",
    packages=find_packages(),
    install_requires=install_requires(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": ["srt-reserve=SRT.cli.reserve:main"],
    },
)
