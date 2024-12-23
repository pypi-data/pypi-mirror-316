from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="suits",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "shutup"
    ],
    description="Ask Donna to do things for you, instead of worrying about pesky syntactical mumbo-jumbo. NOT intended for production purposes.",
    author="Ishan Sandeep Kshirsagar",
    author_email="ishank20062002@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
)