from __future__ import absolute_import
# --------------------------------------------------------
#    a8_menu - QGIS plugins menu class
#
#    begin                : August 5, 2009
#    copyright            : (c) 2009 - 2012 by Michael Minn
#    email                : See michaelminn.com
#
#   MMQGIS is free software and is offered without guarantee
#   or warranty. You can redistribute it and/or modify it 
#   under the terms of version 2 of the GNU General Public 
#   License (GPL v2) as published by the Free Software 
#   Foundation (www.gnu.org).
# --------------------------------------------------------
import os
from builtins import object
from qgis import core, gui
from qgis.PyQt import QtCore, QtGui, QtWidgets

from .encodedpolylinedialog import encodedPolylineDialog

class encodedPolyline_menu(object):
    
	def __init__(self, iface):
		self.iface = iface
		self.a8_menu = None

	def add_submenu(self, submenu):
		if self.a8_menu != None:
			self.a8_menu.addMenu(submenu)
		else:
			self.iface.addPluginToMenu("&Encoded Polyline Builder", submenu.menuAction())

	def initGui(self):
            #self.a8_menu = QMenu(QCoreApplication.translate("pv", "Encoded Polyline Builder"))
            #self.iface.mainWindow().menuBar().insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.a8_menu)

            #self.import_export_menu = QMenu(QCoreApplication.translate("Encoded Polyline Builder", "&Encoded Polyline Builder"))
            #self.add_submenu(self.import_export_menu)

            icon = QtGui.QIcon(os.path.dirname(__file__) + "/icon.png")
            # self.encodedPolylineAction = QtGui.QAction(icon, "Encoded Polyline Builder", self.iface.mainWindow())
            # self.encodedPolylineAction.triggered.connect(self.initiateEncodedPolylineDialog)
            #self.import_export_menu.addAction(self.encodedPolylineAction)
            
            # self.iface.addPluginToVectorMenu("&Encoded Polyline", self.encodedPolylineAction)
            # self.iface.addToolBarIcon(self.encodedPolylineAction)

	def unload(self):
		#if self.a8_menu != None:
		#self.iface.mainWindow().menuBar().removeAction(self.a8_menu.menuAction())
		#else:
			#self.iface.removePluginMenu("&Encoded Polyline Builder", self.import_export_menu.menuAction())

		# This one button in the plugins toolbar is for the South Derbyshire District Council (7/14/2013)
		# self.iface.removeToolBarIcon(self.encodedPolylineAction)
		print( "this unload" )

	def initiateEncodedPolylineDialog(self):
		dialog = encodedPolylineDialog(self.iface)
		dialog.exec_()


