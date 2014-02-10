# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_encodedpolyline.ui'
#
# Created: Sun Feb 02 15:58:15 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_encodedPolyline(object):
    def setupUi(self, encodedPolyline):
        encodedPolyline.setObjectName(_fromUtf8("Encoded Polyline Builder"))
        encodedPolyline.resize(376, 190)
        self.buttonBox = QtGui.QDialogButtonBox(encodedPolyline)
        self.buttonBox.setGeometry(QtCore.QRect(110, 150, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.outputFileBrowse = QtGui.QPushButton(encodedPolyline)
        self.outputFileBrowse.setGeometry(QtCore.QRect(280, 70, 79, 26))
        self.outputFileBrowse.setObjectName(_fromUtf8("outputFileBrowse"))
        self.outputFilename = QtGui.QLineEdit(encodedPolyline)
        self.outputFilename.setGeometry(QtCore.QRect(10, 70, 261, 21))
        self.outputFilename.setReadOnly(False)
        self.outputFilename.setObjectName(_fromUtf8("outputFilename"))
        self.outputFileDescriptor = QtGui.QLabel(encodedPolyline)
        self.outputFileDescriptor.setGeometry(QtCore.QRect(10, 50, 151, 22))
        self.outputFileDescriptor.setObjectName(_fromUtf8("outputFileDescriptor"))
        self.sourceLayerDescriptor = QtGui.QLabel(encodedPolyline)
        self.sourceLayerDescriptor.setGeometry(QtCore.QRect(10, 0, 108, 22))
        self.sourceLayerDescriptor.setObjectName(_fromUtf8("sourceLayerDescriptor"))
        self.sourceLayer = QtGui.QComboBox(encodedPolyline)
        self.sourceLayer.setGeometry(QtCore.QRect(10, 20, 351, 27))
        self.sourceLayer.setObjectName(_fromUtf8("sourceLayer"))
        self.outputFieldPrefix = QtGui.QLineEdit(encodedPolyline)
        self.outputFieldPrefix.setGeometry(QtCore.QRect(10, 120, 351, 21))
        self.outputFieldPrefix.setReadOnly(False)
        self.outputFieldPrefix.setObjectName(_fromUtf8("outputFieldPrefix"))
        self.outputFieldPrefixDescriptor = QtGui.QLabel(encodedPolyline)
        self.outputFieldPrefixDescriptor.setGeometry(QtCore.QRect(10, 100, 151, 22))
        self.outputFieldPrefixDescriptor.setObjectName(_fromUtf8("outputFieldPrefixDescriptor"))

        self.retranslateUi(encodedPolyline)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), encodedPolyline.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), encodedPolyline.reject)
        QtCore.QMetaObject.connectSlotsByName(encodedPolyline)

    def retranslateUi(self, encodedPolyline):
        encodedPolyline.setWindowTitle(_translate("encodedPolyline", "encodedPolyline", None))
        self.outputFileBrowse.setText(_translate("encodedPolyline", "Browse...", None))
        self.outputFilename.setText(_translate("encodedPolyline", "boundaries.csv", None))
        self.outputFileDescriptor.setText(_translate("encodedPolyline", "Output CSV File", None))
        self.sourceLayerDescriptor.setText(_translate("encodedPolyline", "Source Layer", None))
        self.outputFieldPrefix.setText(_translate("encodedPolyline", "", None))
        self.outputFieldPrefixDescriptor.setText(_translate("encodedPolyline", "Field Name Prefix (optional)", None))
	