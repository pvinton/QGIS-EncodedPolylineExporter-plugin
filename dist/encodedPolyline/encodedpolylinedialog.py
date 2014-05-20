# -*- coding: utf-8 -*-
"""
/***************************************************************************
 encodedPolylineDialog
                                 A QGIS plugin
 Export a vector layer to a .csv file in Encoded Polyline format
                             -------------------
        begin                : 2014-02-02
        copyright            : (C) 2014 by Patrick Vinton
        email                : patrickvinton@hotmail.com
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

import csv
import os
import inspect
import operator

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

import resources

from ui_encodedpolyline import Ui_encodedPolyline
from encodedpolyline import encodedPolyline_export_to_csv


class encodedPolylineDialog(QDialog, Ui_encodedPolyline):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        QObject.connect(self.outputFileBrowse, SIGNAL("clicked()"), self.browseOutputFile)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.run)
        QObject.connect(self.sourceLayer, SIGNAL("currentIndexChanged(QString)"), self.updateOutputFieldPrefix)

        load_combo_box_with_vector_layers(self.iface, self.sourceLayer, True)
        
        #message =  os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        paramsFile = os.path.dirname(__file__) + "/LastOutputFileLocation.txt"
        paramsFile = open(paramsFile, "r")
        lastExportLocation = paramsFile.readline()
        paramsFile.close()
        
        #qgis.mainWindow().statusBar().showMessage(message)
        #self.iface.messageBar().pushMessage(message, 0, 5)

        
        if self.sourceLayer.currentText().__len__() == 0:
            #self.outputFilename.setText(os.getcwd() + "/Boundaries.csv")
            self.outputFilename.setText(lastExportLocation + "/Boundaries.csv")
        else:
            #self.outputFilename.setText(os.getcwd() + "/" + self.sourceLayer.currentText() + ".csv")
            self.outputFilename.setText(lastExportLocation + "/" + self.sourceLayer.currentText() + ".csv")

    def browseOutputFile(self):
        newname = QFileDialog.getSaveFileName(None, "Output CSV File", 
            self.outputFilename.displayText(), "CSV File (*.csv)")

        if newname != None:
                    self.outputFilename.setText(newname)    

    def updateOutputFieldPrefix(self):
        paramsFile = os.path.dirname(__file__) + "/LastOutputFileLocation.txt"
        paramsFile = open(paramsFile, "r")
        lastExportLocation = paramsFile.readline()
        paramsFile.close()
    
        layer = find_layer(self.sourceLayer.currentText())
        #self.outputFilename.setText(os.getcwd() + "/" + self.sourceLayer.currentText() + ".csv")
        self.outputFilename.setText(lastExportLocation + "/" + self.sourceLayer.currentText() + ".csv")
        self.outputFieldPrefix.setText(self.sourceLayer.currentText())
        

                
    def run(self):
        delimiter = ","
        lineterminator = "\n"
        sourceLayer = self.sourceLayer.currentText()
        outputFilename = self.outputFilename.displayText()
        outputFieldPrefix = self.outputFieldPrefix.displayText()
        simplifyGeom = self.checkBox.checkState()
        
        message = encodedPolyline_export_to_csv(self.iface, sourceLayer, outputFilename, outputFieldPrefix, simplifyGeom, delimiter, lineterminator)
        if message <> None:
            QMessageBox.critical(self.iface.mainWindow(), "Geometry Export", message)


def load_combo_box_with_vector_layers(qgis, combo_box, set_selected):
    for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
        if layer.type() == QgsMapLayer.VectorLayer:
            combo_box.addItem(layer.name())
    
    if (type(set_selected) != bool):
        combo_index = combo_box.findText(set_selected)
        if combo_index >= 0:
            combo_box.setCurrentIndex(combo_index)
            return;

    for index, layer in enumerate(qgis.legendInterface().selectedLayers()):
        combo_index = combo_box.findText(layer.name())
        if combo_index >= 0:
            combo_box.setCurrentIndex(combo_index)
            break;


def find_layer(layer_name):
    # print "find_layer(" + str(layer_name) + ")"

    for name, search_layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
        if search_layer.name() == layer_name:
            return search_layer

    return None