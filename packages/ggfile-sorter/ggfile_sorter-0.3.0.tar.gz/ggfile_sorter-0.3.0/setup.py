from setuptools import setup, find_packages

setup(
    name="ggfile-sorter",
    version="0.3.0",
    packages=find_packages(),
    description="A library for sorting files based on their extensions, size, or date.",
    long_description="This library allows you to sort files in a directory by their type (e.g., images, documents, audio files) or by their size or modification date.",
    author="Nikita",
    author_email="firi8228@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
