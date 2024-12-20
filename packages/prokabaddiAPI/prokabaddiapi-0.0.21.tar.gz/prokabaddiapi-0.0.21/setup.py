from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.21'
DESCRIPTION = ' Real time stats scraper of all prokabaddi seasons'
LONG_DESCRIPTION = 'This is a powerful tool designed to extract comprehensive data about players and teams from the official Pro prokabaddiAPI website. This library is engineered to provide detailed insights into prokabaddiAPI, including player statistics, team performance metrics, and match results. It offers a streamlined and efficient way to gather and analyze prokabaddiAPI data, which is crucial for sports analytics and machine learning applications.'

# Setting up
setup(
    name="prokabaddiAPI",
    version=VERSION,
    author="Abhineet Raj",
    author_email="<abhineetraj5032@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['socket', 'selenium'],
    keywords=['prokabaddi', 'API', 'kabaddi', 'scraping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)