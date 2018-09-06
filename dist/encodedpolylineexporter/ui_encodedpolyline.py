# Form implementation generated from reading ui file '.\ui_encodedpolyline.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog;

class Ui_encodedPolyline(QDialog):
    def setupUi(self, encodedPolyline):
        encodedPolyline.setObjectName("encodedPolyline")
        encodedPolyline.resize(376, 190)
        self.buttonBox = QtWidgets.QDialogButtonBox(encodedPolyline)
        self.buttonBox.setGeometry(QtCore.QRect(110, 150, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.outputFileBrowse = QtWidgets.QPushButton(encodedPolyline)
        self.outputFileBrowse.setGeometry(QtCore.QRect(280, 70, 79, 26))
        self.outputFileBrowse.setObjectName("outputFileBrowse")
        self.outputFilename = QtWidgets.QLineEdit(encodedPolyline)
        self.outputFilename.setGeometry(QtCore.QRect(10, 70, 261, 21))
        self.outputFilename.setReadOnly(False)
        self.outputFilename.setObjectName("outputFilename")
        self.outputFileDescriptor = QtWidgets.QLabel(encodedPolyline)
        self.outputFileDescriptor.setGeometry(QtCore.QRect(10, 50, 151, 22))
        self.outputFileDescriptor.setObjectName("outputFileDescriptor")
        self.sourceLayerDescriptor = QtWidgets.QLabel(encodedPolyline)
        self.sourceLayerDescriptor.setGeometry(QtCore.QRect(10, 0, 108, 22))
        self.sourceLayerDescriptor.setObjectName("sourceLayerDescriptor")
        self.sourceLayer = QtWidgets.QComboBox(encodedPolyline)
        self.sourceLayer.setGeometry(QtCore.QRect(10, 20, 351, 27))
        self.sourceLayer.setObjectName("sourceLayer")
        self.outputFieldPrefix = QtWidgets.QLineEdit(encodedPolyline)
        self.outputFieldPrefix.setGeometry(QtCore.QRect(10, 120, 351, 21))
        self.outputFieldPrefix.setReadOnly(False)
        self.outputFieldPrefix.setObjectName("outputFieldPrefix")
        self.outputFieldPrefixDescriptor = QtWidgets.QLabel(encodedPolyline)
        self.outputFieldPrefixDescriptor.setGeometry(QtCore.QRect(10, 100, 151, 22))
        self.outputFieldPrefixDescriptor.setObjectName("outputFieldPrefixDescriptor")

        self.retranslateUi(encodedPolyline)
        self.buttonBox.accepted.connect(encodedPolyline.accept)
        self.buttonBox.rejected.connect(encodedPolyline.reject)
        QtCore.QMetaObject.connectSlotsByName(encodedPolyline)

    def retranslateUi(self, encodedPolyline):
        _translate = QtCore.QCoreApplication.translate
        encodedPolyline.setWindowTitle(_translate("encodedPolyline", "encodedPolyline"))
        self.outputFileBrowse.setText(_translate("encodedPolyline", "Browse..."))
        self.outputFilename.setText(_translate("encodedPolyline", "boundaries.csv"))
        self.outputFileDescriptor.setText(_translate("encodedPolyline", "Output CSV File"))
        self.sourceLayerDescriptor.setText(_translate("encodedPolyline", "Source Layer"))
        self.outputFieldPrefix.setText(_translate("encodedPolyline", "boundaries.csv"))
        self.outputFieldPrefixDescriptor.setText(_translate("encodedPolyline", "Field Name Prefix (optional)"))

