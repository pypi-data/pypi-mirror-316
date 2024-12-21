from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    long_description = f.read()

setup(
    name="encapsulation",  # Replace with your own package name
    version="0.2.2",
    author="Seb Wiechers",
    author_email="",
    description="Encapsulation and decorators made easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/JungeWerther/From",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
