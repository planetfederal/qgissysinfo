#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import qgisinfo
import systeminfo

class QgisSysInfoTests(unittest.TestCase):

    def setUp(self):
        pass

    def testQgisInfo(self):
        info = qgisinfo.allQgisInfo()
        self.assertTrue("QGIS settings" in info)
        self.assertTrue("QGIS providers" in info)
        self.assertTrue("QGIS information" in info)
        self.assertTrue("QGIS plugins" in info)

    def testSystemInfo(self):
        info = qgisinfo.allQgisInfo()
        self.assertTrue("Python information" in info)
        self.assertTrue("Qt/PyQt information" in info)
        self.assertTrue("System information" in info)

def testSuite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(QgisSysInfoTests, 'test'))
    return suite

