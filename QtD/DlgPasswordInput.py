# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgPasswordInput.ui'
#
# Created: Tue Oct  7 14:39:06 2014
#      by: PyQt4 UI code generator 4.11.1
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

class Ui_DlgPasswordInput(object):
    def setupUi(self, DlgPasswordInput):
        DlgPasswordInput.setObjectName(_fromUtf8("DlgPasswordInput"))
        DlgPasswordInput.resize(202, 85)
        self.txtPassword = QtGui.QLineEdit(DlgPasswordInput)
        self.txtPassword.setGeometry(QtCore.QRect(10, 30, 191, 23))
        self.txtPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPassword.setObjectName(_fromUtf8("txtPassword"))
        self.lblPassword = QtGui.QLabel(DlgPasswordInput)
        self.lblPassword.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.lblPassword.setObjectName(_fromUtf8("lblPassword"))
        self.btnChange = QtGui.QPushButton(DlgPasswordInput)
        self.btnChange.setGeometry(QtCore.QRect(110, 60, 91, 24))
        self.btnChange.setObjectName(_fromUtf8("btnChange"))

        self.retranslateUi(DlgPasswordInput)
        QtCore.QMetaObject.connectSlotsByName(DlgPasswordInput)

    def retranslateUi(self, DlgPasswordInput):
        DlgPasswordInput.setWindowTitle(_translate("DlgPasswordInput", "Dialog", None))
        self.lblPassword.setText(_translate("DlgPasswordInput", "Podaj nowe hasło:", None))
        self.btnChange.setText(_translate("DlgPasswordInput", "Zmień", None))

