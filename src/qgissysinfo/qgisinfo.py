# -*- coding: utf-8 -*-

"""
***************************************************************************
    qgisinfo.py
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
import ConfigParser

from qgis.core.contextmanagers import qgisapp
from qgis.core import QGis, QgsApplication, QgsProviderRegistry
import qgis.utils

from PyQt4.QtCore import QSettings


reposGroup = "/Qgis/plugin-repos"


def allQgisInfo():
    """Returns all possible QGIS information.
    """

    info = qgisMainInfo()
    info.update(qgisSettingsInfo())
    info.update(qgisPluginsInfo())
    info.update(qgisProvidersInfo())

    return info

def qgisSettingsInfo():
    """Returns various bits of information from QGIS settings.
    This information can be retrieved even if QGIS can not start.
    """

    settings = QSettings("QGIS", "QGIS2")

    repos = []
    settings.beginGroup(reposGroup)
    for key in settings.childGroups():
        repoUrl = settings.value(key + "/url", "", type=str)
        authcfg = settings.value(key + "/authcfg", "", type=str)
        isEnabled = settings.value(key + "/enabled", True, type=bool)
        repos.append(
                "{name}: {url} ({enabled}, {auth})".format(
                        name=key,
                        url=repoUrl,
                        enabled="enabled" if isEnabled else "disabled",
                        auth="need auth" if authcfg != "" else "no auth"))
    settings.endGroup()

    return {"QGIS Settings": {"Plugin repositories": repos}


def qgisProvidersInfo():
    """Returns information about various QGIS plugins (data providers,
    installed and active plugins, etc).
    """

    try:
        with qgisapp(sys.argv):
            providers = QgsProviderRegistry.instance().pluginList().split('\n')
    except:
        providers = ["Could not load QGIS data provider plugins"]

    return {"QGIS providers": {"Available QGIS data provider plugins": providers}


def qgisMainInfo():
    """Returns general QGIS information like version, code revision,
    lib and app paths, etc.
    """

    try:
        with qgisapp(sys.argv):
            appState = QgsApplication.showSettings().replace("\t\t", " ").split("\n")[1:]
            prefixPath = QgsApplication.prefixPath()
            libraryPath = QgsApplication.libraryPath()
            libExecPath = QgsApplication.libexecPath()
            pkgDataPath = QgsApplication.pkgDataPath()
    except:
        appState = ["Could not read QGIS settings"]
        prefixPath = "Not available"
        libraryPath = "Not available"
        libExecPath = "Not available"
        pkgDataPath = "Not available"

    return {"QGIS information": {"QGIS version": "{} ({})".format(QGis.QGIS_VERSION, QGis.QGIS_DEV_VERSION),
                                "QGIS prefix path": prefixPath,
                                "QGIS library path": libraryPath,
                                "QGIS lib exec path": libExecPath,
                                "QGIS pkg data path": pkgDataPath,
                                "QGIS application state": appState}}


def qgisPluginsInfo():
    cfg = ConfigParser.SafeConfigParser()

    pluginPaths = []
    try:
        with qgisapp(sys.argv):
            pluginPaths = qgis.utils.plugin_paths
            pkgDataPath = QgsApplication.pkgDataPath()
    except:
        if len(pluginPaths) == 0:
            pluginPaths.append(os.path.join(os.path.expanduser("~"), ".qgis2", "python", "plugins"))
        if pkgDataPath != "":
            pluginPaths.append(os.path.join(pkgDataPath, "python", "plugins"))

    availablePythonPlugins = []
    for p in pluginPaths:
        for (root, dirs, files) in os.walk(p):
            for d in dirs:
                pluginPath = os.path.join(root, d)
                version = cfg.read(os.path.join(pluginPath, 'metadata.txt'))
                availablePythonPlugins.append("{} ({}) from {}".format(d, version, pluginPath))

    activePythonPlugins = []
    settings = QSettings("QGIS", "QGIS2")
    settings.beginGroup("PythonPlugins")
    for p in settings.childKeys():
        if settings.value(p, True, type=bool):
            activePythonPlugins.append(p)
    settings.endGroup()
    if len(activePythonPlugins) == 0:
        activePythonPlugins = ["There are no active Python plugins"]

    activeCppPlugins = []
    settings = QSettings("QGIS", "QGIS2")
    settings.beginGroup("Plugins")
    for p in settings.childKeys():
        if settings.value(p, True, type=bool):
            activeCppPlugins.append(p)
    settings.endGroup()
    if len(activeCppPlugins) == 0:
        activeCppPlugins = ["There are no active C++ plugins"]

    return{"QGIS Plugins":{            
                "Available Python plugins": availablePythonPlugins,            
                "Active Python plugins": activePythonPlugins,            
                "Active C++ plugins": activeCppPlugins}}

    
