# -*- coding: utf-8 -*-
'''
Created on 29 cze 2014

@author: codedigger
'''

from PyQt4 import QtGui, QtCore
import bcrypt
from db import db
from statics import statics

class LoginWindow(QtGui.QDialog):
  def __init__(self):
    super(LoginWindow, self).__init__()

    self.resize(350,150)
    self.setWindowTitle("Logowanie do systemu")

    self.vlayout=QtGui.QHBoxLayout()

    self.loginPanel=QtGui.QWidget()
    self.loginPanelLayout=QtGui.QFormLayout()
    self.loginPanel.setLayout(self.loginPanelLayout)

    self.login=QtGui.QLineEdit()
    self.password=QtGui.QLineEdit()
    self.password.setEchoMode(QtGui.QLineEdit.Password)

    self.btnAnuluj=QtGui.QPushButton("Anuluj")
    self.btnZaloguj=QtGui.QPushButton("Zaloguj")

    self.buttony=QtGui.QDialogButtonBox()
    self.buttony.setStandardButtons(QtGui.QDialogButtonBox.Abort|
                                    #QtGui.QDialogButtonBox.Reset|
                                    QtGui.QDialogButtonBox.Yes)
    self.buttony.rejected.connect(self.clkReject)
    self.buttony.accepted.connect(self.clkAccept)

    self.loginPanelLayout.addRow("Login: ", self.login)
    self.loginPanelLayout.addRow("Hasło: ", self.password)
    self.loginPanelLayout.addRow(" ", QtGui.QWidget())
    self.loginPanelLayout.addRow(" ", self.buttony)
    self.loginPanelLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)

    self.logo=QtGui.QLabel("")
    self.logo.setPixmap(QtGui.QPixmap("../gfx/img/32WOG-logo.png"))

    self.vlayout.addWidget(self.logo)
    self.vlayout.addWidget(self.loginPanel)

    self.setLayout(self.vlayout)

  def check(self, login, password):
    session=db.Session()
    try:
      user=session.query(db.User).filter(db.User.login==login).one()
    except:
      user=None
    session.close()
    if user and user.isPasswordCorrect(password):
      statics.currentLogedUser=user
      return True
    else: return False

  def clkReject(self):
    self.done(0)

  def clkAccept(self):
    if self.check(self.login.text(), self.password.text()):
      self.done(1)
    else:
      self.done(2)



#Do przetestowania - potem usunąć
if __name__ == '__main__':
  import sys
  app = QtGui.QApplication(sys.argv)
  w=LoginWindow()
  w.show()
  sys.exit(app.exec_())