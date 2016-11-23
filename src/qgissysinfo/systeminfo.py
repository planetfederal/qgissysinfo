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

import cpuinfo

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

    physical, logical = _cpuCount()
    return {"System information": {
                "Operating system": platform.platform(),
                "Processor": cpuinfo.get_cpu_info()['brand'],
                "CPU cores" : "{} (total), {} (physical)".format(logical, physical),
                "Installed RAM": _bytes2human(_ramSize()),
                "Hostname": platform.node(),
                "User name": getpass.getuser(),
                "Home directory": os.path.expanduser("~")}}


def pythonInfo():
    """Returns Python information.
    """
    return {"Python information":{
                "Python implementation": platform.python_implementation(),
                "Python version": "{} {}".format(platform.python_version(),
                                                platform.python_build()),
                "Python binary path": sys.executable,
                "Prefix": sys.prefix,
                "Exec prefix": sys.exec_prefix,
                "Module search paths": sys.path}}

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


def _ramSize():
    osType = platform.system()
    if osType == "Windows":
        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ('dwLength', c_ulong),
                ('dwMemoryLoad', c_ulong),
                ('dwTotalPhys', c_ulong),
                ('dwAvailPhys', c_ulong),
                ('dwTotalPageFile', c_ulong),
                ('dwAvailPageFile', c_ulong),
                ('dwTotalVirtual', c_ulong),
                ('dwAvailVirtual', c_ulong)
            ]

        memoryStatus = MEMORYSTATUS()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
        return memoryStatus.dwTotalPhys
    elif osType == "Linux":
        value = os.popen("free -b").readlines()[1].split()[1]
        return int(value)
    elif osType == "Darwin":
        value = os.popen("sysctl hw.memsize").readlines().split(":")[1].strip()
        return int(value)


def _cpuCount():
    osType = platform.system()
    if osType == "Windows":
        values = os.popen("wmic cpu get NumberOfCores,NumberOfLogicalProcessors").readlines()[1].split()
        physical = values[0].strip()
        logical = values[1].strip()
    elif osType == "Linux":
        physical = os.popen("cat /proc/cpuinfo | grep 'cpu cores' | uniq").readlines().split(":")[1].strip()
        logical = os.popen("grep -c 'processor' /proc/cpuinfo").readlines()
    elif osType == "Darwin":
        physical = os.popen("sysctl -n hw.physicalcpu").readlines()
        logical = os.popen("sysctl -n hw.logicalcpu").readlines()
    return physical, logical

