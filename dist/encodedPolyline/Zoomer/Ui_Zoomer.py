# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file Ui_Zoomer.ui
# Created with: PyQt4 UI code generator 4.4.4
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Zoomer(object):
    def setupUi(self, Zoomer):
        Zoomer.setObjectName("Zoomer")
        Zoomer.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Zoomer)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Zoomer)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Zoomer.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Zoomer.reject)
        QtCore.QMetaObject.connectSlotsByName(Zoomer)

    def retranslateUi(self, Zoomer):
        Zoomer.setWindowTitle(QtGui.QApplication.translate("Zoomer", "Zoomer", None, QtGui.QApplication.UnicodeUTF8))
