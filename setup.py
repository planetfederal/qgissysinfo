import os
from setuptools import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="qgissysinfo",
    version="0.1",
    install_requires=[],
    author="Alexander Bruy",
    author_email="alexbruy@boundlessgeo.com",
    description="Collect system and QGIS information",    
    long_description=(read('README')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    license="GPL3",
    keywords="QGIS",
    url='https://github.com/boundlessgeo/qgissysinfo',
    package_dir={'': 'src'},
    test_suite='test.suite',
    packages=['qgissysinfo',]
)
