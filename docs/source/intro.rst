Introduction
============

*qgissysinfo* is a Python package which makes it easier for users/devs
collect various information about platform and environment in which QGIS
application is running.

If QGIS is not installed or can not be started, tool will collect only
information, which does not require access to the QGIS application
instance.

Usage
=====

There is a command line tool called ``genreport`` which will collect all
available information and store it in the text file inside user home
directory. Report files have standard name ``QgisSystemReport-YYYY-MM-DD-N.txt``,
where YYYY-MM-DD replaced with current date and N replaced with report
number.

Also libary can be used programmaticaly. There are two modules:

* *systeminfo* for getting general system info
* *qgisinfo* for retrieving information about QGIS

Each module provides number of functions for retrieving various pieces
of information as well as function for retrieving all information from
single call. In the ``qgissysinfo`` package there is also function ``info()``
which will return all information about system and QGIS.

Information returned as dictionary object, to convert it to plain text
use ``info_as_text()`` function from ``qgissysinfo`` package.
