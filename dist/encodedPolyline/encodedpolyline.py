# -*- coding: utf-8 -*-
"""
/***************************************************************************
 encodedPolyline
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


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources
import csv
#from encodedpolylinedialog import encodedPolylineDialog
import os.path
import time


class encodedPolyline:

    def __init__(self, iface):
        self.iface = iface
		
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'encodedpolyline_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = encodedPolylineDialog(iface)
	

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/encodedpolyline/icon.png"),
            u"Encoded Polyline Exporter", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Encoded Polyline Exporter", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Encoded Polyline Exporter", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
			

def encodedPolyline_export_to_csv(qgis, layername, node_filename, outputFieldPrefix, simplifyGeom, field_delimiter, line_terminator):
    layer = find_layer(layername)
    
    if (layer == None) or (layer.type() != QgsMapLayer.VectorLayer):
        return "Invalid Vector Layer " + layername
    
    
    forwardSlashIndex = node_filename[::-1].find("/")
    backSlashIndex = node_filename[::-1].find("\\") 
    
    if forwardSlashIndex < 0:
        forwardSlashIndex = 9999999
    
    if backSlashIndex < 0:
        backSlashIndex = 9999999
    
    if forwardSlashIndex < backSlashIndex:
        slashIndex = forwardSlashIndex+1
    else:
        slashIndex = backSlashIndex+1
        
    nodefile = open(node_filename, 'w')
 
    paramsFile = os.path.dirname(__file__) + "/LastOutputFileLocation.txt"
    paramsFile = open(paramsFile, "w")
    outputPath = node_filename[0:-slashIndex]
    paramsFile.write(outputPath)
    paramsFile.close()
    
    outputFilePrefix = node_filename[:-4]


    if simplifyGeom == 2:
        thresholds = [0,0.00001,0.00002,0.00003,0.00004,0.00005,0.00006,0.00007,0.00008,0.00009,0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,10,20]
        tolerances = [0,0.00005,0.000065,0.00008,0.000095,0.00011,0.000125,0.00014,0.000155,0.00017,0.0002,0.00025,0.0003,0.00035,0.0004,0.00045,0.0005,0.00055,0.0006,0.00065,0.00088,0.00111,0.00134,0.00157,0.0018,0.00203,0.00226,0.00249,0.003,0.0034,0.0038,0.0042,0.0046,0.005,0.0054,0.0058,0.0062,0.007,0.0087,0.0104,0.0121,0.0138,0.0155,0.0172,0.0189,0.0206,0.0223,0.0273,0.0323,0.0373,0.045,0.1]
        
        qgis.mainWindow().statusBar().showMessage('Saving temporary shapefile...') 
        QgsVectorFileWriter.writeAsVectorFormat(layer, outputFilePrefix+"_temp.shp", "utf-8", None, "ESRI Shapefile")
        
        qgis.mainWindow().statusBar().showMessage('Loading temporary shapefile...')
        layer = QgsVectorLayer(outputFilePrefix+"_temp.shp", time.strftime("%H%M%S"), "ogr")
        layer.startEditing()
      
        i=0
        feature_index = 0
        feature_count = layer.dataProvider().featureCount()
        while i<len(tolerances)-1:
            tolerance = tolerances[i];
            lowerThreshold = str(thresholds[i]);
            upperThreshold = str(thresholds[i+1]);
            thresholdExpression = '$area>'+lowerThreshold+' and $area<='+upperThreshold
             
            request = QgsFeatureRequest().setFilterExpression(thresholdExpression)
            features = layer.getFeatures(request)
            for feature in features:
                feature_index +=1
                if (feature_index % 10) == 0:
                    message = "Simplifying feature " + unicode(feature_index) + " of " + unicode(feature_count)
                    message += ' (' + thresholdExpression + ')'
                    qgis.mainWindow().statusBar().showMessage(message)
                
                fid = feature.id()
                fgeom = feature.geometry()
                if (fgeom.isGeosValid() and not fgeom.isGeosEmpty()):
                    fSimpGeom = fgeom.simplify(tolerance)
                    layer.changeGeometry(fid, fSimpGeom)
                    #feature.setGeometry(fSimpGeom)
                    #layer.updateFeature(feature)
            i += 1
            
        qgis.mainWindow().statusBar().showMessage('Committing simplifications...')
        layer.commitChanges()
        
        qgis.mainWindow().statusBar().showMessage('Saving simplified shapefile...')
        QgsVectorFileWriter.writeAsVectorFormat(layer, outputFilePrefix+"_simplified.shp", "utf-8", None, "ESRI Shapefile")

    
    attribute_header = []
    for index, field in enumerate(layer.dataProvider().fields()):
        if (layer.geometryType() == QGis.Point):
            node_header.append(field.name())
        else:
            attribute_header.append(field.name()) 
     
    attribute_header.append(outputFieldPrefix + "Boundary")
    attribute_header.append(outputFieldPrefix + "CenterLat")
    attribute_header.append(outputFieldPrefix + "CenterLng")
    node_writer = csv.writer(nodefile, delimiter = field_delimiter, lineterminator = '\n', quoting=csv.QUOTE_NONNUMERIC)
    node_writer.writerow(attribute_header)
 
 
 
    feature_type = ""
    feature_count = layer.dataProvider().featureCount()
    for feature_index, feature in enumerate(layer.dataProvider().getFeatures()):
        if (feature_index % 10) == 0:
            message = "Exporting feature " + unicode(feature_index) + " of " + unicode(feature_count)
            qgis.mainWindow().statusBar().showMessage(message)
 
        if (feature.geometry() == None):
            return "Cannot export layer with no shape data"
 
        elif (feature.geometry().wkbType() == QGis.WKBLineString) or \
             (feature.geometry().wkbType() == QGis.WKBLineString25D):
             
            ring_number = 0
            polyline = feature.geometry().asPolyline()
            
            if(feature.geometry().centroid() is not None):
                centroidLat = str(feature.geometry().centroid().asPoint().y())
                centroidLng = str(feature.geometry().centroid().asPoint().x())
            else:
                centroidLat = ''
                centroidLng = ''
             
            shape_id = unicode(feature_index)
            row = [ ]
            for attindex, attribute in enumerate(feature.attributes()):
                if type(attribute) == float:
                    if attribute - round(attribute) == 0:
                        attribute = int(round(attribute))
 
                row.append(unicode(attribute).encode("utf-8"))
             
            encodedPolyline = ""
             
            if ring_number > 0:
                shape_id = shape_id + ".ring" + unicode(ring_number)
            ring_number = ring_number + 1
             
            plat = 0
            plng = 0
 
            for point in polyline:
                lat = float(point.y())
                lng = float(point.x())
                 
                plate5 = round(plat * 100000)
                plnge5 = round(plng * 100000)
                late5 = round(lat * 100000)
                lnge5 = round(lng * 100000)
 
                dlat = late5 - plate5
                dlng = lnge5 - plnge5
 
                encodedLat = encodeCoord(dlat)
                encodedLng = encodeCoord(dlng)
                 
                encodedPolyline += encodedLat
                encodedPolyline += encodedLng
                 
                plat = lat
                plng = lng
                 
            encodedPolyline += '<br>'
             
            encodedPolyline = encodedPolyline[0:-4]
            row.append(encodedPolyline)
            row.append(centroidLat)
            row.append(centroidLng)
            node_writer.writerow(row)
 
        elif (feature.geometry().wkbType() == QGis.WKBMultiLineString) or \
             (feature.geometry().wkbType() == QGis.WKBMultiLineString25D):
            polylines = feature.geometry().asMultiPolyline()
            centroidLat = str(feature.geometry().centroid().asPoint().y())
            centroidLng = str(feature.geometry().centroid().asPoint().x())
            encodedPolyline = ""
             
            for polyline_index, polyline in enumerate(polylines):
                ring_number = 0
 
                shape_id = unicode(feature_index) + "." + unicode(polyline_index)
                if ring_number > 0:
                    shape_id = shape_id + ".ring" + unicode(ring_number)
                ring_number = ring_number + 1
                 
                plat = 0
                plng = 0
 
                for point in polyline:
                    lat = float(point.y())
                    lng = float(point.x())
                     
                    plate5 = round(plat * 100000)
                    plnge5 = round(plng * 100000)
                    late5 = round(lat * 100000)
                    lnge5 = round(lng * 100000)
 
                    dlat = late5 - plate5
                    dlng = lnge5 - plnge5
 
                    encodedLat = encodeCoord(dlat)
                    encodedLng = encodeCoord(dlng)
                     
                    encodedPolyline += encodedLat
                    encodedPolyline += encodedLng
                     
                    plat = lat
                    plng = lng
                     
                encodedPolyline += '<br>'
                 
                row = [ ]
                for attindex, attribute in enumerate(feature.attributes()):
                    if type(attribute) == float:
                        if attribute - round(attribute) == 0:
                            attribute = int(round(attribute))
                         
                    row.append(unicode(attribute).encode("utf-8"))
             
            encodedPolyline = encodedPolyline[0:-4]        
            row.append(encodedPolyline)
            row.append(centroidLat)
            row.append(centroidLng)
            node_writer.writerow(row)
 
        elif (feature.geometry().wkbType() == QGis.WKBPolygon) or \
             (feature.geometry().wkbType() == QGis.WKBPolygon25D):
            # The first polyline in the polygon is the outer ring
            # Subsequent polylines (if any) are inner rings (holes)
            ring_number = 0
            polygon = feature.geometry().asPolygon()
            
            #if (fgeom.isGeosValid() and not fgeom.isGeosEmpty()):
            #print type(feature.geometry().centroid())
            if(feature.geometry().centroid() is not None):
                centroidLat = str(feature.geometry().centroid().asPoint().y())
                centroidLng = str(feature.geometry().centroid().asPoint().x())
            else:
                centroidLat = ''
                centroidLng = '' 
             
            shape_id = unicode(feature_index)
            row = [ ]
            for attindex, attribute in enumerate(feature.attributes()):
                if type(attribute) == float:
                    if attribute - round(attribute) == 0:
                        attribute = int(round(attribute))
 
                row.append(unicode(attribute).encode("utf-8"))
             
            encodedPolyline = ""
             
            for polyline in polygon:
                 
                if ring_number > 0:
                    shape_id = shape_id + ".ring" + unicode(ring_number)
                ring_number = ring_number + 1
                 
                plat = 0
                plng = 0
                 
 
                for point in polyline:
                    lat = float(point.y())
                    lng = float(point.x())
                     
                    plate5 = round(plat * 100000)
                    plnge5 = round(plng * 100000)
                    late5 = round(lat * 100000)
                    lnge5 = round(lng * 100000)
 
                    dlat = late5 - plate5
                    dlng = lnge5 - plnge5
 
                    encodedLat = encodeCoord(dlat)
                    encodedLng = encodeCoord(dlng)
                     
                    encodedPolyline += encodedLat
                    encodedPolyline += encodedLng
                     
                    plat = lat
                    plng = lng
                     
                encodedPolyline += '<br>'
             
            encodedPolyline = encodedPolyline[0:-4]
            row.append(encodedPolyline)
            row.append(centroidLat)
            row.append(centroidLng)
            node_writer.writerow(row)
                 
 
        elif (feature.geometry().wkbType() == QGis.WKBMultiPolygon) or \
             (feature.geometry().wkbType() == QGis.WKBMultiPolygon25D):
            multipolygon = feature.geometry().asMultiPolygon()
            
            if(feature.geometry().centroid() is not None): 
                centroidLat = str(feature.geometry().centroid().asPoint().y())
                centroidLng = str(feature.geometry().centroid().asPoint().x())
            else:
                centroidLat = ''
                centroidLng = ''
                
            encodedPolyline = ""
                 
            for polygon_index, polygon in enumerate(multipolygon):
                ring_number = 0
 
                for polyline in polygon:
                    shape_id = unicode(feature_index) + "." + unicode(polygon_index)
                    if ring_number > 0:
                        shape_id = shape_id + ".ring" + unicode(ring_number)
                    ring_number = ring_number + 1
                     
                    plat = 0
                    plng = 0
 
                    for point in polyline:
                        lat = float(point.y())
                        lng = float(point.x())
                         
                        plate5 = round(plat * 100000)
                        plnge5 = round(plng * 100000)
                        late5 = round(lat * 100000)
                        lnge5 = round(lng * 100000)
 
                        dlat = late5 - plate5
                        dlng = lnge5 - plnge5
 
                        encodedLat = encodeCoord(dlat)
                        encodedLng = encodeCoord(dlng)
                         
                        encodedPolyline += encodedLat
                        encodedPolyline += encodedLng
                         
                        plat = lat
                        plng = lng
                         
                    encodedPolyline += '<br>'
                     
                    row = [ ]
                    for attindex, attribute in enumerate(feature.attributes()):
                        if type(attribute) == float:
                            if attribute - round(attribute) == 0:
                                attribute = int(round(attribute))
                             
                        row.append(unicode(attribute).encode("utf-8"))
             
            encodedPolyline = encodedPolyline[0:-4]        
            row.append(encodedPolyline)
            row.append(centroidLat)
            row.append(centroidLng)
            node_writer.writerow(row)
 
                     
 
        else:
            return "Unsupported geometry" 
             
    del nodefile
    
    
    if simplifyGeom == 2:
        qgis.mainWindow().statusBar().showMessage('Unloading temporary shapefile...')
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        
        qgis.mainWindow().statusBar().showMessage('Deleting temporary shapefile...')
        os.remove(outputFilePrefix+'_temp.cpg')
        #os.remove(outputFilePrefix+'_temp.dbf')
        os.remove(outputFilePrefix+'_temp.prj')
        os.remove(outputFilePrefix+'_temp.qpj')
        #os.remove(outputFilePrefix+'_temp.shp')
        #os.remove(outputFilePrefix+'_temp.shx')
        os.remove(outputFilePrefix+'_simplified.cpg')
        os.remove(outputFilePrefix+'_simplified.prj')
        os.remove(outputFilePrefix+'_simplified.qpj')
        
    
    message = unicode(feature_count) + " records exported"
    qgis.mainWindow().statusBar().showMessage(message)
    qgis.messageBar().pushMessage(message, 0, 3)

        
    return None

    
def encodeCoord(x):
    encoded_point = ""
    x = int(round(x))
    x = x<<1
    
    if x<0:
        x = ~x

    while x >= 32:
        z = x&31
        z = z|32
        z = z+63
        z = chr(z)
        encoded_point += z

        x = x>>5

    z = x+63
    z = chr(z)
    encoded_point += z
    return encoded_point


def find_layer(layer_name):
    for name, search_layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
        if search_layer.name() == layer_name:
            return search_layer

    return None