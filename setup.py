from setuptools import find_packages, setup


def long_descrtiption():
    with open("README.md", "r", encoding="utf-8") as f:
        desc = f.read()
    return desc


setup(
    name="SRTrain",
    author="ryanking13",
    author_email="def6488@gmail.com",
    version="1.0.2",
    description="SRT(Super Rapid Train) wrapper for python",
    long_description=long_descrtiption(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/ryanking13/SRT",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ],
)
