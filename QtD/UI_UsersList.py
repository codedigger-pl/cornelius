# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uzytkownicy.ui'
#
# Created: Tue Oct  7 13:00:32 2014
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

class Ui_Uzytkownicy(object):
    def setupUi(self, Uzytkownicy):
        Uzytkownicy.setObjectName(_fromUtf8("Uzytkownicy"))
        Uzytkownicy.setWindowModality(QtCore.Qt.NonModal)
        Uzytkownicy.resize(298, 453)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.tblUsers = QtGui.QTableWidget(self.dockWidgetContents)
        self.tblUsers.setGeometry(QtCore.QRect(-5, 1, 301, 391))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblUsers.sizePolicy().hasHeightForWidth())
        self.tblUsers.setSizePolicy(sizePolicy)
        self.tblUsers.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblUsers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblUsers.setCornerButtonEnabled(False)
        self.tblUsers.setColumnCount(4)
        self.tblUsers.setObjectName(_fromUtf8("tblUsers"))
        self.tblUsers.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblUsers.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblUsers.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblUsers.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tblUsers.setHorizontalHeaderItem(3, item)
        self.tblUsers.verticalHeader().setVisible(False)
        self.btnUserPassChange = QtGui.QPushButton(self.dockWidgetContents)
        self.btnUserPassChange.setGeometry(QtCore.QRect(200, 400, 91, 24))
        self.btnUserPassChange.setObjectName(_fromUtf8("btnUserPassChange"))
        self.btnUserAdd = QtGui.QPushButton(self.dockWidgetContents)
        self.btnUserAdd.setGeometry(QtCore.QRect(0, 400, 91, 24))
        self.btnUserAdd.setObjectName(_fromUtf8("btnUserAdd"))
        Uzytkownicy.setWidget(self.dockWidgetContents)

        self.retranslateUi(Uzytkownicy)
        QtCore.QMetaObject.connectSlotsByName(Uzytkownicy)

    def retranslateUi(self, Uzytkownicy):
        Uzytkownicy.setWindowTitle(_translate("Uzytkownicy", "Użytkownicy systemu", None))
        self.tblUsers.setToolTip(_translate("Uzytkownicy", "Lista użytkowników systemu", None))
        self.tblUsers.setSortingEnabled(True)
        item = self.tblUsers.horizontalHeaderItem(0)
        item.setText(_translate("Uzytkownicy", "Login", None))
        item = self.tblUsers.horizontalHeaderItem(1)
        item.setText(_translate("Uzytkownicy", "Imię", None))
        item = self.tblUsers.horizontalHeaderItem(2)
        item.setText(_translate("Uzytkownicy", "Nazwisko", None))
        item = self.tblUsers.horizontalHeaderItem(3)
        item.setText(_translate("Uzytkownicy", "Administrator", None))
        self.btnUserPassChange.setText(_translate("Uzytkownicy", "Zmień hasło", None))
        self.btnUserAdd.setText(_translate("Uzytkownicy", "Dodaj", None))

