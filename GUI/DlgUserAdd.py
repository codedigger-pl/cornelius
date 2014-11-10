'''
Created on 8 paź 2014

@author: codedigger
'''

from QtD.DlgUserAdd import Ui_DlgUserAdd
from PyQt4 import QtGui
from db import db

class DlgUserAdd(Ui_DlgUserAdd, QtGui.QDialog):
  def __init__(self):
    super(DlgUserAdd, self).__init__()
#     super(QtGui.QDialog, self).__init__()
    self.setupUi(self)
    self.btnAddUser.clicked.connect(self.userAddClicked)

  def userAddClicked(self):
    if self.txtFirstName.text()==''   or      \
       self.txtLastName.text()==''    or      \
       self.txtLogin.text()==''       or      \
       self.txtPassword1.text()==''   or      \
       self.txtPassword2.text()=='':
      messageBox=QtGui.QMessageBox(self)
      messageBox.setText('Należy wypełnić wszystkie pola dotyczące danych użytkownika')
      messageBox.exec()
#       self.done(0)
    elif self.txtPassword1.text()!=self.txtPassword2.text():
      messageBox=QtGui.QMessageBox(self)
      messageBox.setText('Wpisane hasła nie pasują. Proszę wpisać identyczne hasła')
      messageBox.exec()
#       self.done(0)
    elif not db.isLoginFree(self.txtLogin.text()):
      messageBox=QtGui.QMessageBox(self)
      messageBox.setText('Podany login jest już zajęty')
      messageBox.exec()
#       self.done(0)
    else: self.done(1)

  def getLogin(self): return self.txtLogin.text()
  def getFirstName(self): return self.txtFirstName.text()
  def getLastName(self): return self.txtLastName.text()
  def getIsAdmin(self): return self.chkIsAdmin.isChecked()
  def getPassword(self): return self.txtPassword1.text()