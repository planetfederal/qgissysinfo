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
import ConfigParser

from qgis.core.contextmanagers import qgisapp
from qgis.core import QGis, QgsApplication, QgsProviderRegistry
from qgis.utils import plugin_paths

from PyQt4.QtCore import QSettings


reposGroup = "/Qgis/plugin-repos"


def qgisSettingsInfo():
    """Returns various bits of information from QGIS settings.
    This information can be retrieved even if QGIS can not start.
    """
    info = ["QGIS settings",
            "-------------",
            "Plugin repositories:",
            "{qgisRepos}",
           ]

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
                        enabled=isEnabled,
                        auth=True if authcfg != "" else False))
    settings.endGroup()

    repos = os.linesep.join(["\t{}".format(i) for i in repos])

    info = os.linesep.join(info)
    info = info.format(qgisRepos=repos,
                      )
    return info


def qgisProvidersInfo():
    """Returns information about various QGIS plugins (data providers,
    installed and active plugins, etc).
    """
    info = ["QGIS providers",
            "--------------",
            "Available QGIS data provider plugins:",
            "{dataProviders}",
           ]

    with qgisapp(sys.argv):
        providers = QgsProviderRegistry.instance().pluginList().split('\n')

    providers = os.linesep.join(["\t{}".format(i) for i in providers])

    info = os.linesep.join(info)
    info = info.format(dataProviders=providers,
                      )
    return info


def qgisMainInfo():
    """Returns general QGIS information like version, code revision,
    lib and app paths, etc.
    """
    info = ["QGIS information",
            "----------------",
            "QGIS version: {qgisVersion}",
            "QGIS prefix path: {qgisPrefixPath}",
            "QGIS library path: {qgisLibraryPath}",
            "QGIS lib exec path: {qgisLibExecPath}",
            "QGIS application state:"
            "{qgisAppState}",
           ]

    appState = QgsApplication.showSettings().replace("\t\t", " ").split("\n")[1:]
    appState = os.linesep.join(["\t{}".format(i) for i in appState])

    info = os.linesep.join(info)
    info = info.format(qgisVersion="{} ({})".format(QGis.QGIS_VERSION, QGis.QGIS_DEV_VERSION),
                       qgisPrefixPath=QgsApplication.prefixPath(),
                       qgisLibraryPath=QgsApplication.libraryPath(),
                       qgisLibExecPath=QgsApplication.libexecPath(),
                       qgisAppState=appState
                      )
    return info


def qgisPluginsInfo():
    cfg = ConfigParser.SafeConfigParser()

    availablePythonPlugins = []
    for p in plugin_paths:
        for (root, dirs, files) in os.walk(p):
            for d in dirs:
                pluginPath = os.path.join(root, d)
                version = cfg.read(os.path.join(pluginPath, 'metadata.txt'))
                availablePythonPlugins.append("{} ({}) from {}".format(d, version, pluginPath))

    availablePythonPlugins = os.linesep.join(["\t{}".format(i) for i in availablePythonPlugins])

    activePythonPlugins = []
    settings = QSettings("QGIS", "QGIS2")
    settings.beginGroup("PythonPlugins")
    for p in settings.childKeys():
        if settings.value(p, True, type=bool):
            activePythonPlugins.append(p)
    settings.endGroup()
    activePythonPlugins = os.linesep.join(["\t{}".format(i) for i in activePythonPlugins])

    activeCppPlugins = []
    settings = QSettings("QGIS", "QGIS2")
    settings.beginGroup("Plugins")
    for p in settings.childKeys():
        if settings.value(p, True, type=bool):
            activeCppPlugins.append(p)
    settings.endGroup()
    activeCppPlugins = os.linesep.join(["\t{}".format(i) for i in activeCppPlugins])

    info = ["QGIS Plugins",
            "------------",
            "Available Python plugins:",
            "{availPythonPlugins}",
            "Active Python plugins:"
            "{activePythonPlugins}",
            "Active C++ plugins:"
            "{activeCppPlugins}",
           ]

    info = os.linesep.join(info)
    info = info.format(availPythonPlugins=,
                       activePythonPlugins=,
                       activeCppPlugins=
                      )
    return info
