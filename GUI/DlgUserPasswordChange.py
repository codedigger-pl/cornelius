# -*- coding: utf-8 -*-

from statics.statics import currentLogedUser

###############################################################################
# DlgUserPasswordChange.py
#
# author: Paweł Surowiec (codedigger)
# creation date: 10.11.2014
# version: 0.0.1
#
# Module contains dialog allowing user change his password.
# More info: this dialog checks, if entered password is correct and change
# password for user from static.currentLogedUser
#
# Calling this module directly, will call this dialog with some example
# user. Info are send to console
###############################################################################

DLGUSERPASSWORDCHANGE_PY_VERSION=(0,0,1)

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from QtD.DlgUserPasswordChange import Ui_DlgUserPasswordChange
from db import db
from statics import statics

# if __name__!='__main__':
#   from statics.statics import currentLogedUser
# else:
#   currentLogedUser=db.User()
#   currentLogedUser.password=currentLogedUser.encryptPassword('admin')

class DlgUserPasswordChange(Ui_DlgUserPasswordChange, QtGui.QDialog):
  """Dialog allowing user change his own password. Current logged user is in
  static module"""

  def __init__(self):
    super(DlgUserPasswordChange, self).__init__()
    self.setupUi(self)

    self.btnChange.clicked.connect(self.changeButtonClicked)


  @pyqtSlot()
  def changeButtonClicked(self):
    """Action after click "Change" button"""
    # given password is correct?
    if not statics.currentLogedUser.isPasswordCorrect(self.txtOldPassword.text()):
      message=QtGui.QMessageBox(self)
      message.setText('Podane hasło nie jest prawidłowe')
      message.exec_()

    # given two new passwords are the same?
    elif self.txtNewPassword.text()!=self.txtNewPasswordRep.text():
      message=QtGui.QMessageBox(self)
      message.setText('Podane nowe hasła nie są takie same')
      message.exec_()

    # changing password in database
    else:
      session=db.Session()
      session.add(statics.currentLogedUser)
      statics.currentLogedUser.password=statics.currentLogedUser.encryptPassword(self.txtNewPassword.text())
      session.commit()
      session.close()
      self.done(1)

# running dialog like application
if __name__=='__main__':
  import sys
  app = QtGui.QApplication(sys.argv)
  print(DlgUserPasswordChange().exec_())
  sys.exit(app.exec_())
