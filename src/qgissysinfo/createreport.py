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

import sip
for c in ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"):
    sip.setapi(c, 2)

reportsDir = os.path.expanduser("~")


def createReport():
    import qgissysinfo

    i = 1
    fileName = "QgisSystemReport-{}-{}.txt".format(datetime.date.today().isoformat(), i)
    fullPath = os.path.join(reportsDir, fileName)
    while os.path.exists(fullPath):
        i += 1
        fileName = "QgisSystemReport-{}-{}.txt".format(datetime.date.today().isoformat(), i)
        fullPath = os.path.join(reportsDir, fileName)

    report = qgissysinfo.info_as_text()
    with codecs.open(fullPath, "w", "utf-8") as f:
        f.write(report)

    return report, fullPath


if __name__ == '__main__' and __package__ is None:
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    report, filePath = createReport()
    print "Report saved saved to {}".format(filePath)
