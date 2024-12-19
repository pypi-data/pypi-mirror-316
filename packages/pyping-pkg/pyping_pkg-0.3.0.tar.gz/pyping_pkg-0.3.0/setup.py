from setuptools import setup, find_packages

MODULE = "pyping_pkg"
VERSION = "0.3.0"
DESCRIPTION = "Pyping_pkg is a module used to check projects PyPi web site informations as if already exists and your respective versions."
LONG_DESCRIPTION = "Pyping_pkg is a module used to check projects PyPi web site informations as if already exists and your respective versions."
AUTHOR = "Natanael Quintino"
AUTHOR_EMAIL = "natanael.quintino@ipiaget.pt"
LICENSE = "MIT License"
REQUIREMENTS = "'build', 'twine'"
KEYWORDS = "pypi, automation, install, packages, module"

setup(
    name=MODULE,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=find_packages(
        include=[MODULE, MODULE+'.*']
    ),
    install_requires=eval('''[
        %s
    ]''' % REQUIREMENTS),
    keywords=KEYWORDS,
    classifiers= [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)