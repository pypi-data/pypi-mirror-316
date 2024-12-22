from setuptools import setup, find_packages


version = {}
with open("version.py") as version_file:
    exec(version_file.read(), version)

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pycrystalpay',
    version=version['__version__'],
    description='CrystalPay api wrapper',
    author='Lisica',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='nomail@google.com',
    url='https://github.com/mrsmori/pycrystalpay',
    install_requires=(
        "httpx==0.28.1",
        "pydantic==2.10.4"
    ),
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)