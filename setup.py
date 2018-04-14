from setuptools import setup, find_packages

# setup the project
setup(
    name="syncit",
    version="1.0.3",
    url="https://github.com/shhaumb/syncit",
    author="Shubham Jain",
    author_email="sj.iitr@gmail.com",
    description=(
        "Extract synchronous functions from async coroutine functions "
        "using AST manipulation"),
    keywords="asyncio synchronous ast syncit",
    license="MIT",
    packages=find_packages(include=['syncit']),
    py_modules=['syncit'],
    python_requires='>=3.5'
)
