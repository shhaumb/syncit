from setuptools import setup, find_packages

# setup the project
setup(
    name="syncit",
    version="1.0.0",
    author="Shubham Jain",
    description=(
        "Extract synchronous functions from async coroutine functions "
        "using AST manipulation"),
    license="MIT",
    packages=find_packages(include=['syncit']),
)
