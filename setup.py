# author https://github.com/MIrrox27/Axiom
# setup.py


from setuptools import setup, find_packages
from axiom import __version__

with open("README.md", 'r', encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="axiom",
    version=__version__,
    description="Axiom Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Maksim Pronkin",
    author_email="", # почту пока не добавляю
    url="https://github.com/MIrrox27/Axiom",

    packages=find_packages(),
    entry_points = {
        "condole_scripts": [
            "axiom = axiom.__main__:main"
        ]
    },

    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[],
)