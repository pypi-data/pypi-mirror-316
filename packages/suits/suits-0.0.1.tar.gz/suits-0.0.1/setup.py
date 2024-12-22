from setuptools import setup, find_packages

setup(
    name="suits",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "google-generativeai"
    ],
    description="Ask Donna to do things for you, instead of worrying about pesky syntactical issues. NOT intended for production purposes.",
    author="Ishan Sandeep Kshirsagar",
    author_email="ishank20062002@gmail.com"
)