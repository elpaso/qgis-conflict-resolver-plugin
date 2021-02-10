# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : ConflictResolver
Description          : ConflictResolver
Date                 : 12/Oct/2020
copyright            : (C) 2020 by ItOpen
email                : elpaso@itopen.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
import sys
import json
from functools import partial
from ctypes import CDLL
from ctypes.util import find_library

from osgeo import gdal
from qgis.core import (
    QgsApplication,
    QgsMapLayer,
    QgsMapLayerType,
    QgsMessageLog,
    QgsProject,
    QgsFeatureRequest,
)


# Import the PyQt and QGIS libraries
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox


class ConflictResolver(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()

        if sys.platform == 'win32':
            soname = os.path.join(os.path.dirname(__file__), 'cpp', 'build', 'libqgispatches.dll')
            libqgispatches = CDLL(soname)
        else:
            soname = os.path.join(os.path.dirname(__file__), 'cpp', 'build', 'libqgispatches.so')
            libqgispatches = CDLL(soname)

        assert libqgispatches
        self.libqgispatches = libqgispatches


    def initGui(self):
        QgsProject.instance().layerWasAdded.connect(self.connectLayer)

    def log(self, message):
        QgsMessageLog.logMessage(json.dumps(message), "ConflictResolver")

    def unload(self):
        # Remove the plugin menu item and icon
        pass

    def checkChanges(self, layer):

        assert layer and layer.isValid()
        self.log("Checking changes for %s" % layer.name())
        buffer = layer.editBuffer()

        ok = True

        if buffer:
            for fid, geom in buffer.changedGeometries().items():
                self.log("FID %s changed" % fid)
                req = QgsFeatureRequest()
                req.setFilterFid(fid)
                old_geom = next(layer.dataProvider().getFeatures(req)).geometry()
                assert old_geom.asWkt() != geom.asWkt()

            for fid, attribute_dict in buffer.changedAttributeValues().items():
                self.log("FID %s changed" % fid)
                req = QgsFeatureRequest()
                req.setFilterFid(fid)
                old_attrs = next(layer.dataProvider().getFeatures(req)).attributes()
                self.log(attribute_dict)

                try:
                    if int(attribute_dict['identifikator']) < 0:
                        self.log('Cannot store negative identifiers!')
                        ok = False
                except KeyError:
                    pass

        layer.setAllowCommit(ok)

    def connectLayer(self, layer):

        self.log("Layer added: %s" % layer.name())

        if layer and layer.type() == QgsMapLayerType.VectorLayer:
            layer.beforeCommitChanges.connect(partial(self.checkChanges, layer))


if __name__ == "__main__":
    pass
