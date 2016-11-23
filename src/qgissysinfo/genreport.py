# -*- coding: utf-8 -*-

"""
***************************************************************************
    genreport.py
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
import codecs
import datetime

import systeminfo

hasPyQgis = False
try:
    import qgisinfo
    hasPyQgis = True
except ImportError:
    pass

reportsDir = os.path.expanduser("~")


def main():
    info = [systeminfo.allSystemInfo()]
    if hasPyQgis:
        info.append(qgisinfo.allQgisInfo())
    info = "/n/n".join(info)

    i = 1
    fileName = "QgisSystemReport-{}-{}.txt".format(datetime.date.today().isoformat(), i)
    fullPath = os.path.join(reportsDir, fileName)
    while os.path.exists(fullPath):
        i += 1
        fileName = "QgisSystemReport-{}-{}.txt".format(datetime.date.today().isoformat(), i)
        fullPath = os.path.join(reportsDir, fileName)

    with codecs.open(fullPath, "w", "utf-8") as f:
        f.write(info)

    print "Information saved to {}".format(fullPath)


if __name__ == "__main__":
    main()
