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
			

def encodedPolyline_export_to_csv(qgis, layername, node_filename, outputFieldPrefix, field_delimiter, line_terminator):
    layer = find_layer(layername)

    if (layer == None) or (layer.type() != QgsMapLayer.VectorLayer):
        return "Invalid Vector Layer " + layername

    attribute_header = []
    for index, field in enumerate(layer.dataProvider().fields()):
        if (layer.geometryType() == QGis.Point):
            node_header.append(field.name())
        else:
            attribute_header.append(field.name())

    nodefile = open(node_filename, 'w')
    
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
            centroidLat = str(feature.geometry().centroid().asPoint().y())
            centroidLng = str(feature.geometry().centroid().asPoint().x())
            
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
            centroidLat = str(feature.geometry().centroid().asPoint().y())
            centroidLng = str(feature.geometry().centroid().asPoint().x())
            
            
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
            
            centroidLat = str(feature.geometry().centroid().asPoint().y())
            centroidLng = str(feature.geometry().centroid().asPoint().x())
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