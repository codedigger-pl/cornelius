# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgUserPasswordChange.ui'
#
# Created: Mon Nov 10 15:36:58 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DlgUserPasswordChange(object):
    def setupUi(self, DlgUserPasswordChange):
        DlgUserPasswordChange.setObjectName(_fromUtf8("DlgUserPasswordChange"))
        DlgUserPasswordChange.resize(328, 126)
        DlgUserPasswordChange.setMinimumSize(QtCore.QSize(328, 126))
        DlgUserPasswordChange.setMaximumSize(QtCore.QSize(328, 126))
        self.btnChange = QtGui.QPushButton(DlgUserPasswordChange)
        self.btnChange.setGeometry(QtCore.QRect(220, 100, 99, 23))
        self.btnChange.setObjectName(_fromUtf8("btnChange"))
        self.widget = QtGui.QWidget(DlgUserPasswordChange)
        self.widget.setGeometry(QtCore.QRect(10, 10, 311, 24))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.txtOldPassword = QtGui.QLineEdit(self.widget)
        self.txtOldPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.txtOldPassword.setObjectName(_fromUtf8("txtOldPassword"))
        self.horizontalLayout.addWidget(self.txtOldPassword)
        self.widget1 = QtGui.QWidget(DlgUserPasswordChange)
        self.widget1.setGeometry(QtCore.QRect(10, 50, 311, 24))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget1)
        self.label_2.setMinimumSize(QtCore.QSize(130, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.txtNewPassword = QtGui.QLineEdit(self.widget1)
        self.txtNewPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.txtNewPassword.setObjectName(_fromUtf8("txtNewPassword"))
        self.horizontalLayout_2.addWidget(self.txtNewPassword)
        self.widget2 = QtGui.QWidget(DlgUserPasswordChange)
        self.widget2.setGeometry(QtCore.QRect(10, 70, 311, 24))
        self.widget2.setObjectName(_fromUtf8("widget2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.widget2)
        self.label_3.setMinimumSize(QtCore.QSize(130, 0))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.txtNewPasswordRep = QtGui.QLineEdit(self.widget2)
        self.txtNewPasswordRep.setEchoMode(QtGui.QLineEdit.Password)
        self.txtNewPasswordRep.setObjectName(_fromUtf8("txtNewPasswordRep"))
        self.horizontalLayout_3.addWidget(self.txtNewPasswordRep)

        self.retranslateUi(DlgUserPasswordChange)
        QtCore.QMetaObject.connectSlotsByName(DlgUserPasswordChange)

    def retranslateUi(self, DlgUserPasswordChange):
        DlgUserPasswordChange.setWindowTitle(QtGui.QApplication.translate("DlgUserPasswordChange", "Zmiana hasła", None, QtGui.QApplication.UnicodeUTF8))
        self.btnChange.setText(QtGui.QApplication.translate("DlgUserPasswordChange", "Zmień", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DlgUserPasswordChange", "Dotychczasowe hasło:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DlgUserPasswordChange", "Nowe hasło", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DlgUserPasswordChange", "Powtórz nowe hasło:", None, QtGui.QApplication.UnicodeUTF8))

