from setuptools import setup

setup(
    name="termux-color",
    version="0.1.0",
    py_modules=["color"],
    description="A simple Python module for color manipulation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sakib Salim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
