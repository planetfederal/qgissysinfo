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
import configparser

import sip
for c in ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"):
    sip.setapi(c, 2)

from qgis.core import Qgis, QgsApplication, QgsProviderRegistry, QgsAuthManager
from qgis.utils import iface

from PyQt5.QtCore import QSettings


reposGroup = "/Qgis/plugin-repos"

def _profilePath():
    if os.name == 'nt':
        return os.path.expanduser('~/AppData/Roaming/QGIS/QGIS3/profiles/default')
    else:
        return os.path.expanduser('~/.local/share/QGIS/QGIS3/profiles/default')    

def _settings():
    return QSettings(os.path.join(_profilePath(), "QGIS", "QGIS3.ini"), QSettings.IniFormat)

def allQgisInfo():
    """Returns all possible QGIS information.
    """

    info = qgisMainInfo()
    info.update(qgisSettingsInfo())
    info.update(qgisPluginsInfo())
    info.update(qgisProvidersInfo())
    info.update(qgisAuthPluginsInfo())

    return info


def qgisSettingsInfo():
    """Returns various bits of information from QGIS settings.
    This information can be retrieved even if QGIS can not start.
    """

    settings = _settings()

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

    return {"QGIS settings": {"Plugin repositories": repos}}


def qgisProvidersInfo():
    """Returns information about various QGIS plugins (data providers,
    installed and active plugins, etc).
    """

    if iface is None:
        try:
            app = QgsApplication(sys.argv, False)
            app.initQgis()
            providers = QgsProviderRegistry.instance().pluginList().split('\n')
        except:
            providers = ["Could not load QGIS data provider plugins"]
    else:
        providers = QgsProviderRegistry.instance().pluginList().split('\n')

    return {"QGIS providers": {"Available QGIS data provider plugins": providers}}


def qgisMainInfo():
    """Returns general QGIS information like version, code revision,
    lib and app paths, etc.
    """

    if iface is None:
        try:
            app = QgsApplication(sys.argv, False)
            app.initQgis()
            appState = app.showSettings().replace("\t\t", " ").split("\n")[1:]
            prefixPath = app.prefixPath()
            libraryPath = app.libraryPath()
            libExecPath = app.libexecPath()
            pkgDataPath = app.pkgDataPath()
        except:
            appState = ["Could not read QGIS settings"]
            prefixPath = "Not available"
            libraryPath = "Not available"
            libExecPath = "Not available"
            pkgDataPath = "Not available"
    else:
        appState = QgsApplication.showSettings().replace("\t\t", " ").split("\n")[1:]
        prefixPath = QgsApplication.prefixPath()
        libraryPath = QgsApplication.libraryPath()
        libExecPath = QgsApplication.libexecPath()
        pkgDataPath = QgsApplication.pkgDataPath()

    return {"QGIS information": {"QGIS version": "{} ({})".format(Qgis.QGIS_VERSION, Qgis.QGIS_DEV_VERSION),
                                 "QGIS prefix path": prefixPath,
                                 "QGIS library path": libraryPath,
                                 "QGIS lib exec path": libExecPath,
                                 "QGIS pkg data path": pkgDataPath,
                                 "QGIS application state": appState}}


def qgisPluginsInfo():
    """Returns installed Python plugins, their versions and locations.
    Also returns list of active plugins (both core and Python).
    """
    cfg = configparser.SafeConfigParser()


    pluginPaths = []
    if iface is None:
        try:
            app = QgsApplication(sys.argv, False)
            app.initQgis()
            pluginPaths.append(app.pkgDataPath())
            pluginPaths.append(os.path.split(app.qgisUserDatabaseFilePath())[0])
        except:
            pluginPaths.append(_profilePath())
    else:
        pluginPaths.append(QgsApplication.pkgDataPath())
        pluginPaths.append(os.path.split(QgsApplication.qgisUserDatabaseFilePath())[0])

    pluginPaths = [os.path.join(str(p), "python", "plugins") for p in pluginPaths]

    availablePythonPlugins = []
    for p in pluginPaths:
        for (root, dirs, files) in os.walk(p):
            for d in dirs:
                pluginPath = os.path.join(root, d)
                cfg.read(os.path.join(pluginPath, 'metadata.txt'))
                version = cfg.get('general', 'version')
                availablePythonPlugins.append("{} ({}) in {}".format(d, version, pluginPath))
            break

    activePythonPlugins = []
    settings = _settings()
    settings.beginGroup("PythonPlugins")
    for p in settings.childKeys():
        if settings.value(p, True, type=bool):
            activePythonPlugins.append(p)
    settings.endGroup()
    if len(activePythonPlugins) == 0:
        activePythonPlugins = ["There are no active Python plugins"]

    activeCppPlugins = []
    settings = _settings()
    settings.beginGroup("Plugins")
    for p in settings.childKeys():
        if settings.value(p, True, type=bool):
            activeCppPlugins.append(p)
    settings.endGroup()
    if len(activeCppPlugins) == 0:
        activeCppPlugins = ["There are no active C++ plugins"]

    return{"QGIS plugins":{
                "Available Python plugins": availablePythonPlugins,
                "Active Python plugins": activePythonPlugins,
                "Active C++ plugins": activeCppPlugins}}


def qgisAuthPluginsInfo():
    """Returns information about available QGIS authentication method plugins.
    """

    found = True
    if iface is None:
        try:
            app = QgsApplication(sys.argv, False)
            app.initQgis()
            authPluginKeys = QgsApplication.authManager().authMethodsKeys()
        except:
            found = False
            authPluginKeys = ["Could not load QGIS authentication method plugins"]
    else:
        authPluginKeys = QgsApplication.authManager().authMethodsKeys()

    if found:
        authPluginsInfo = []
        for key in authPluginKeys:
            m = QgsApplication.authManager().authMethod(key)
            authPluginsInfo.append("{}: {}".format(key, m.displayDescription()))
    else:
        authPluginsInfo = authPluginKeys

    return {"QGIS authentication methods": {"Available QGIS authentication plugins": authPluginsInfo}}
