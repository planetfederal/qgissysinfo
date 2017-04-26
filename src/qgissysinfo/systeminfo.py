# -*- coding: utf-8 -*-

"""
***************************************************************************
    systeminfo.py
    ---------------------
    Date                 : November 2016
    Copyright            : (C) 2016 Boundless, http://boundlessgeo.com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'November 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import ctypes
import getpass
import platform
import subprocess

#import cpuinfo

try:
    import psutil
except ImportError:
    class psutil(object):
        @staticmethod
        def cpu_count(a=True):
           return None
        @staticmethod
        def virtual_memory():
           return None

import sip
for c in ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"):
    sip.setapi(c, 2)

from PyQt4.Qt import PYQT_VERSION_STR
from PyQt4.QtCore import QT_VERSION_STR
from sip import SIP_VERSION_STR

from PyQt4.QtGui import QApplication, QImageReader
from PyQt4.QtSql import QSqlDatabase


def allSystemInfo():
    """Returns all possible system information as plain text string.
    """
    info = systemInfo()
    info.update(pythonInfo())
    info.update(qtInfo())
    return info


def systemInfo():
    """Returns general system information as plain text string.
    """

    ram = psutil.virtual_memory()
    if ram is not None:
        ram = _bytes2human(ram[0])
    else:
        ram = "Not available"

    return {"System information": {
                "Operating system": platform.platform(),
                #"Processor": cpuinfo.get_cpu_info()['brand'],
                "Processor": _cpuInfo(),
                "CPU cores" : "{} (total), {} (physical)".format(
                                      psutil.cpu_count() or "Not available",
                                      psutil.cpu_count(True) or "Not available"),
                "Installed RAM": ram,
                "Hostname": platform.node(),
                "User name": getpass.getuser(),
                "Home directory": os.path.expanduser("~")}}


def pythonInfo():
    """Returns Python information.
    """
    try:
        from pip.operations.freeze import freeze
        pipInfo = list()
        for i in freeze():
            pipInfo.append(i)
    except ImportError, e:
        pipInfo = ["Could not get PIP information: {}".format(e.output)]

    return {"Python information":{
                "Python implementation": platform.python_implementation(),
                "Python version": "{} {}".format(platform.python_version(),
                                                platform.python_build()),
                "Python binary path": sys.executable,
                "Prefix": sys.prefix,
                "Exec prefix": sys.exec_prefix,
                "Module search paths": sys.path,
                "pip freeze": pipInfo}}


def qtInfo():
    """Returns Qt/PyQt information.
    """

    return {"Qt/PyQt information":{
                "Qt version": QT_VERSION_STR,
                "PyQt version": PYQT_VERSION_STR,
                "SIP version": SIP_VERSION_STR,
                "Qt library paths": QApplication.libraryPaths(),
                "Qt database plugins":  QSqlDatabase.drivers(),
                "Qt image plugins": QImageReader.supportedImageFormats()}}


def _bytes2human(n):
    """ Converts bytes into human readable string
    Adopted from http://code.activestate.com/recipes/578019
     """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "{:.1f} {:s}".format(value, s)
    return "{} B".format(n)

def _cpuInfo():
    osType = platform.system()
    if osType == "Windows":
        try:
            info = subprocess.Popen("wmic cpu get Name", shell=True, universal_newlines=True).communicate()[0]
        except subprocess.CalledProcessError, e:
            print "Could not get CPU brand: {}".format(e.output)
            info = "Not available"
    elif osType == "Linux":
        try:
            info = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | uniq", shell=True, universal_newlines=True).split(":")[1].strip()
        except subprocess.CalledProcessError, e:
            print "Could not get CPU brand: {}".format(e.output)
            info = "Not available"
    elif osType == "Darwin":
        try:
            info = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True, universal_newlines=True).split(":")[1].strip()
        except subprocess.CalledProcessError, e:
            print "Could not get CPU brand: {}".format(e.output)
            info = "Not available"
    return info
