# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EncodedPolylineExporterDialog
                                 A QGIS plugin
 Export a vector layer to a .csv file in Encoded Polyline format, with optional geometry simplification
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-04-26
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Patrick Vinton
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
import os.path

from qgis import core, gui
from qgis.core import QgsMessageLog, QgsWkbTypes

def encodedPolylineExport( selfIface, layername, node_filename, outputFieldPrefix, field_delimiter, line_terminator ):
    layer = find_layer(layername)
    
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

    if (layer == None) or (layer.type() != core.QgsMapLayer.VectorLayer):
        return "Invalid Vector Layer " + layername

    attribute_header = []
    for index, field in enumerate(layer.dataProvider().fields()):
        if (layer.geometryType() == core.QgsPoint):
            node_header.append(field.name())
        else:
            attribute_header.append(field.name())

    nodefile = open(node_filename, 'w')

    paramsFile = os.path.dirname(__file__) + "/LastOutputFileLocation.txt"
    with open(paramsFile, 'w') as f:
        f.write(node_filename[0:-slashIndex])
    
    attribute_header.append(outputFieldPrefix + "Boundary")
    attribute_header.append(outputFieldPrefix + "CenterLat")
    attribute_header.append(outputFieldPrefix + "CenterLng")
    node_writer = csv.writer(nodefile, delimiter = field_delimiter, lineterminator = '\n', quoting=csv.QUOTE_NONNUMERIC)
    node_writer.writerow(attribute_header)

    QgsMessageLog.logMessage("Your plugin code has been executed correctly", 'EPE', level=0)
    QgsMessageLog.logMessage("LineString: " + str(QgsWkbTypes.LineString), 'EPE', level=0)

    feature_type = ""
    feature_count = layer.dataProvider().featureCount()
    for feature_index, feature in enumerate(layer.dataProvider().getFeatures()):

        QgsMessageLog.logMessage("Feature type is: " + str(feature.geometry().wkbType()), 'EPE', level=0)

        if (feature_index % 10) == 0:
            message = "Exporting feature " + str(feature_index) + " of " + str(feature_count)
            selfIface.statusBarIface().showMessage( message, 1000 )

        if (feature.geometry() == None):
            QgsMessageLog.logMessage("Feature has no geometry", 'EPE', level=0)
            nodefile.close() 
            del nodefile
            return "Cannot export layer with no shape data"

        elif (feature.geometry().wkbType() == QgsWkbTypes.LineString) or \
            (feature.geometry().wkbType() == QgsWkbTypes.LineString25D):
            QgsMessageLog.logMessage("Feature is LineString", 'EPE', level=0)
            ring_number = 0
            polyline = feature.geometry().asPolyline()
            centroidLat = str(feature.geometry().centroid().asPoint().y())
            centroidLng = str(feature.geometry().centroid().asPoint().x())
            
            shape_id = str(feature_index)
            row = [ ]
            for attindex, attribute in enumerate(feature.attributes()):
                if type(attribute) == float:
                    if attribute - round(attribute) == 0:
                        attribute = int(round(attribute))

                row.append(str(attribute).encode("utf-8"))
            
            encodedPolyline = ""
            
            if ring_number > 0:
                shape_id = shape_id + ".ring" + str(ring_number)
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

        elif (feature.geometry().wkbType() == QgsWkbTypes.MultiLineString) or \
            (feature.geometry().wkbType() == QgsWkbTypes.MultiLineString25D):
            QgsMessageLog.logMessage("Feature is MultiLineString", 'EPE', level=0)
            polylines = feature.geometry().asMultiPolyline()
            centroidLat = str(feature.geometry().centroid().asPoint().y())
            centroidLng = str(feature.geometry().centroid().asPoint().x())
            encodedPolyline = ""
            
            for polyline_index, polyline in enumerate(polylines):
                ring_number = 0

                shape_id = str(feature_index) + "." + str(polyline_index)
                if ring_number > 0:
                    shape_id = shape_id + ".ring" + str(ring_number)
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
                        
                    row.append(str(attribute).encode("utf-8"))
            
            encodedPolyline = encodedPolyline[0:-4]        
            row.append(encodedPolyline)
            row.append(centroidLat)
            row.append(centroidLng)
            node_writer.writerow(row)

        elif (feature.geometry().wkbType() == QgsWkbTypes.Polygon) or \
            (feature.geometry().wkbType() == QgsWkbTypes.Polygon25D):
            QgsMessageLog.logMessage("Feature is Polygon", 'EPE', level=0)
            # The first polyline in the polygon is the outer ring
            # Subsequent polylines (if any) are inner rings (holes)
            ring_number = 0
            polygon = feature.geometry().asPolygon()
            centroidLat = str(feature.geometry().centroid().asPoint().y())
            centroidLng = str(feature.geometry().centroid().asPoint().x())
            
            
            shape_id = str(feature_index)
            row = [ ]
            for attindex, attribute in enumerate(feature.attributes()):
                if type(attribute) == float:
                    if attribute - round(attribute) == 0:
                        attribute = int(round(attribute))

                row.append(str(attribute).encode("utf-8"))
            
            encodedPolyline = ""
            
            for polyline in polygon:
                
                if ring_number > 0:
                    shape_id = shape_id + ".ring" + str(ring_number)
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
                

        elif (feature.geometry().wkbType() == QgsWkbTypes.MultiPolygon) or \
            (feature.geometry().wkbType() == QgsWkbTypes.MultiPolygon25D):
            QgsMessageLog.logMessage("Feature is MultiPolygon", 'EPE', level=0)
            multipolygon = feature.geometry().asMultiPolygon()
            
            centroidLat = str(feature.geometry().centroid().asPoint().y())
            centroidLng = str(feature.geometry().centroid().asPoint().x())
            encodedPolyline = ""
                
            for polygon_index, polygon in enumerate(multipolygon):
                ring_number = 0

                for polyline in polygon:
                    shape_id = str(feature_index) + "." + str(polygon_index)
                    if ring_number > 0:
                        shape_id = shape_id + ".ring" + str(ring_number)
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
                            
                        row.append(attribute)
            
            encodedPolyline = encodedPolyline[0:-4]        
            row.append(encodedPolyline)
            row.append(centroidLat)
            row.append(centroidLng)
            node_writer.writerow(row)

                    

        else:
            QgsMessageLog.logMessage("Feature has unsupported geometry", 'EPE', level=0)
            # nodefile.close() 
            # del nodefile
            # return "Unsupported geometry" 
            continue

    QgsMessageLog.logMessage("Closing nodefile", 'EPE', level=0)
    nodefile.close() 
    del nodefile
    
    message = str(feature_count) + " records exported"
    selfIface.statusBarIface().showMessage( message, 5000 )
    # qgis.messageBar().pushMessage(message, 0, 3)

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
    # print "find_layer(" + str(layer_name) + ")"

    for name, layer in list(core.QgsProject.instance().mapLayers().items()):
        if layer.name() == layer_name:
            return layer

    return None