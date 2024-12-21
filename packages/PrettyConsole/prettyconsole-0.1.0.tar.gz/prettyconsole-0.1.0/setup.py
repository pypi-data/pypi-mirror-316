from setuptools import setup, find_packages

setup(
    name="PrettyConsole",
    version="0.1.0",
    description="A easy way to use colors in the terminal via ANSI Escape Codes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Erick Fernando Carvalho Sanchez",
    author_email="carvalhosanchezerickfernando@gmail.com",
    license="BSD 3-Clause License",
    packages=find_packages(),
    install_requires=[],  # List dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
