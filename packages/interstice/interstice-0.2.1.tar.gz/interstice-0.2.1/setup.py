from setuptools import setup, find_packages

setup(
    name="interstice",
    version="0.2.1",
    description="A game of demons and soldiers on a 10x10 grid.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bananajump",
    author_email="bananajump@bananajump.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
