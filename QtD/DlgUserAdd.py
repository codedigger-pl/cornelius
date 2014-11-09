# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgUserAdd.ui'
#
# Created: Wed Oct  8 09:25:23 2014
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

class Ui_DlgUserAdd(object):
    def setupUi(self, DlgUserAdd):
        DlgUserAdd.setObjectName(_fromUtf8("DlgUserAdd"))
        DlgUserAdd.resize(460, 167)
        self.btnAddUser = QtGui.QPushButton(DlgUserAdd)
        self.btnAddUser.setGeometry(QtCore.QRect(360, 130, 91, 24))
        self.btnAddUser.setObjectName(_fromUtf8("btnAddUser"))
        self.groupBox = QtGui.QGroupBox(DlgUserAdd)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 231, 121))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lblLogin = QtGui.QLabel(self.groupBox)
        self.lblLogin.setGeometry(QtCore.QRect(20, 30, 54, 10))
        self.lblLogin.setObjectName(_fromUtf8("lblLogin"))
        self.txtLogin = QtGui.QLineEdit(self.groupBox)
        self.txtLogin.setGeometry(QtCore.QRect(100, 20, 113, 23))
        self.txtLogin.setObjectName(_fromUtf8("txtLogin"))
        self.lblFirstName = QtGui.QLabel(self.groupBox)
        self.lblFirstName.setGeometry(QtCore.QRect(20, 47, 54, 15))
        self.lblFirstName.setObjectName(_fromUtf8("lblFirstName"))
        self.txtLastName = QtGui.QLineEdit(self.groupBox)
        self.txtLastName.setGeometry(QtCore.QRect(100, 60, 113, 23))
        self.txtLastName.setObjectName(_fromUtf8("txtLastName"))
        self.lblLastName = QtGui.QLabel(self.groupBox)
        self.lblLastName.setGeometry(QtCore.QRect(20, 68, 54, 15))
        self.lblLastName.setObjectName(_fromUtf8("lblLastName"))
        self.chkIsAdmin = QtGui.QCheckBox(self.groupBox)
        self.chkIsAdmin.setGeometry(QtCore.QRect(10, 90, 220, 21))
        self.chkIsAdmin.setObjectName(_fromUtf8("chkIsAdmin"))
        self.txtFirstName = QtGui.QLineEdit(self.groupBox)
        self.txtFirstName.setGeometry(QtCore.QRect(100, 40, 113, 23))
        self.txtFirstName.setObjectName(_fromUtf8("txtFirstName"))
        self.groupBox_2 = QtGui.QGroupBox(DlgUserAdd)
        self.groupBox_2.setGeometry(QtCore.QRect(240, 10, 221, 121))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.lblPassword2 = QtGui.QLabel(self.groupBox_2)
        self.lblPassword2.setGeometry(QtCore.QRect(10, 45, 90, 15))
        self.lblPassword2.setObjectName(_fromUtf8("lblPassword2"))
        self.txtPassword2 = QtGui.QLineEdit(self.groupBox_2)
        self.txtPassword2.setGeometry(QtCore.QRect(100, 40, 113, 23))
        self.txtPassword2.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPassword2.setObjectName(_fromUtf8("txtPassword2"))
        self.lblPassword1 = QtGui.QLabel(self.groupBox_2)
        self.lblPassword1.setGeometry(QtCore.QRect(10, 25, 54, 15))
        self.lblPassword1.setObjectName(_fromUtf8("lblPassword1"))
        self.txtPassword1 = QtGui.QLineEdit(self.groupBox_2)
        self.txtPassword1.setGeometry(QtCore.QRect(100, 20, 113, 23))
        self.txtPassword1.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPassword1.setObjectName(_fromUtf8("txtPassword1"))

        self.retranslateUi(DlgUserAdd)
        QtCore.QMetaObject.connectSlotsByName(DlgUserAdd)
        DlgUserAdd.setTabOrder(self.txtLogin, self.txtFirstName)
        DlgUserAdd.setTabOrder(self.txtFirstName, self.txtLastName)
        DlgUserAdd.setTabOrder(self.txtLastName, self.chkIsAdmin)
        DlgUserAdd.setTabOrder(self.chkIsAdmin, self.txtPassword1)
        DlgUserAdd.setTabOrder(self.txtPassword1, self.txtPassword2)
        DlgUserAdd.setTabOrder(self.txtPassword2, self.btnAddUser)

    def retranslateUi(self, DlgUserAdd):
        DlgUserAdd.setWindowTitle(_translate("DlgUserAdd", "Dialog", None))
        self.btnAddUser.setText(_translate("DlgUserAdd", "Dodaj", None))
        self.groupBox.setTitle(_translate("DlgUserAdd", "Dane Użytkownika", None))
        self.lblLogin.setText(_translate("DlgUserAdd", "Login:", None))
        self.lblFirstName.setText(_translate("DlgUserAdd", "Imię:", None))
        self.lblLastName.setText(_translate("DlgUserAdd", "Nazwisko:", None))
        self.chkIsAdmin.setText(_translate("DlgUserAdd", "Użytkownik jest Administratorem", None))
        self.groupBox_2.setTitle(_translate("DlgUserAdd", "Hasło Użytkownika", None))
        self.lblPassword2.setText(_translate("DlgUserAdd", "Powtórz hasło:", None))
        self.lblPassword1.setText(_translate("DlgUserAdd", "Hasło:", None))

