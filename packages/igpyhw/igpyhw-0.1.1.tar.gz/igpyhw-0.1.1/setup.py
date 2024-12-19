from setuptools import setup, find_packages

setup(
    name="igpyhw",
    version="0.1.1",
    description="A simple example module",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Israel Glixinski",
    author_email="israel_glixinski@hotmail.com",
    url="https://github.com/israelglixinski/igpyhw",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
