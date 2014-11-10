# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgSystemAdd.ui'
#
# Created: Sun Nov  9 18:30:12 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DlgSystemAdd(object):
    def setupUi(self, DlgSystemAdd):
        DlgSystemAdd.setObjectName(_fromUtf8("DlgSystemAdd"))
        DlgSystemAdd.resize(438, 72)
        self.cmbSystems = QtGui.QComboBox(DlgSystemAdd)
        self.cmbSystems.setGeometry(QtCore.QRect(10, 10, 421, 23))
        self.cmbSystems.setObjectName(_fromUtf8("cmbSystems"))
        self.btnAdd = QtGui.QPushButton(DlgSystemAdd)
        self.btnAdd.setGeometry(QtCore.QRect(330, 40, 99, 23))
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))

        self.retranslateUi(DlgSystemAdd)
        QtCore.QMetaObject.connectSlotsByName(DlgSystemAdd)

    def retranslateUi(self, DlgSystemAdd):
        DlgSystemAdd.setWindowTitle(QtGui.QApplication.translate("DlgSystemAdd", "Dodaj system", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("DlgSystemAdd", "Dodaj", None, QtGui.QApplication.UnicodeUTF8))

