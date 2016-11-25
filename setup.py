# -*- coding: utf-8 -*-

import codecs
from setuptools import setup

with codecs.open('README', encoding='utf-8') as f:
    readme_text = f.read()


setup(
    name='qgissysteminfo',
    version='0.1.0',
    install_requires=['psutil', 'py-cpuinfo'],
    author='Alexander Bruy',
    author_email='abruy@boundlessgeo.com',
    description='Collect various information about system and QGIS.',
    long_description=(readme_text),
    entry_points = {'console_scripts': ['genreport=qgissysinfo.genreport:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    license="GPLv3+",
    url='https://github.com/boundlessgeo/qgissysinfo',
    package_dir={'': 'src'},
    packages=['qgissysinfo',]
)
