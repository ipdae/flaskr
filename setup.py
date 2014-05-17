import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "flaskr",
    version = "1.0",
    author = "ipdae",
    author_email = "qooraven@gmail.com",
    description = ("my first web application"),
    license = "BSD",
    keywords = "example documentation tutorial",
    packages=['flaskr'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires = ["flask", "flask-sqlalchemy", "psycopg2"],
)

