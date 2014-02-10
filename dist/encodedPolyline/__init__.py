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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load encodedPolyline class from file encodedPolyline
    from encodedpolyline_menu import encodedPolyline_menu
	#from encodedpolyline import encodedPolyline
    return encodedPolyline_menu(iface)
	#return encodedPolyline(iface)
