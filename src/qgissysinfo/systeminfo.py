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
import getpass
import platform

import cpuinfo
import psutil

from PyQt4.Qt import PYQT_VERSION_STR
from PyQt4.QtCore import QT_VERSION_STR
from sip import SIP_VERSION_STR

from PyQt4.QtGui import QApplication, QImageReader
from PyQt4.QtSql import QSqlDatabase


def systemInfo():
    info = ["System information",
            "------------------",
            "Operating system: {operatingSystem}",
            "Processor: {cpu}",
            "CPU cores: {cores_total} (total), {cores_physical} (physical)"
            "Installed RAM: {ram}",
            "Hostname: {hostname}"
            "User name: {username}",
            "Home directory: {home}"
           ]

    info = os.linesep.join(info)
    info = info.format(operatingSystem=platform.platform(),
                       cpu=cpuinfo.get_cpu_info()['brand'],
                       cores_total=psutil.cpu_count(),
                       cores_physical=psutil.cpu_count(True),
                       ram=_bytes2human(psutil.virtual_memory()[0]),
                       hostname==platform.node(),
                       username=getpass.getuser(),
                       home=os.path.expanduser("~")
                      )
    return info


def pythonInfo():
    info = ["Python information",
            "------------------",
            "Python implementation: {implementation}"
            "Python version: {version} {build}",
            "Python binary path: {binaryPath}",
            "Prefix: {prefix}"
            "Exec prefix: {execPrefix}",
            "Module search paths:",
            "{pythonPath}",
           ]

    modulePaths = os.linesep.join(["\t{}".format(i) for i in sys.path])

    info = os.linesep.join(info)
    info = info.format(implementation=platform.python_implementation(),
                       version=platform.python_version(),
                       build=platform.python_build(),
                       binaryPath=sys.executable,
                       prefix=sys.prefix,
                       execPrefix=sys.exec_prefix,
                       pythonPath=modulePaths
                      )
    return info


def qtInfo():
    info = ["Qt/PyQt information",
            "-------------------",
            "Qt version: {qtVersion}",
            "PyQt version: {pyqtVersion}",
            "SIP version: {sipVersion}",
            "Qt library paths:",
            "{qtLibs}",
            "Qt database plugins:",
            "{qtDbPlugins}",
            "Qt image plugins:",
            "{qtImagePlugins}"
           ]

    libPaths = os.linesep.join(
            ["\t{}".format(i) for i in QApplication.libraryPaths()])
    dbPlugins = os.linesep.join(
            ["\t{}".format(i) for i in QSqlDatabase.drivers()])
    imagePlugins = os.linesep.join(
            ["\t{}".format(i) for i in QImageReader.supportedImageFormats()])

    info = os.linesep.join(info)
    info = info.format(qtVersion=QT_VERSION_STR,
                       pyqtVersion=PYQT_VERSION_STR,
                       sipVersion=SIP_VERSION_STR,
                       qtLibs=libPaths,
                       qtDbPlugins=dbPlugins,
                       qtImagePlugins=imagePlugins
                      )
    return info


def _bytes2human(n):
    """ Adopted from http://code.activestate.com/recipes/578019
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
