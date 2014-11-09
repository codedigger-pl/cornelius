'''
Created on 7 paź 2014

@author: codedigger
'''

from QtD.DlgPasswordInput import Ui_DlgPasswordInput
from PyQt4 import QtGui

class DlgPasswordInput(Ui_DlgPasswordInput, QtGui.QDialog):
  def __init__(self):
    super(DlgPasswordInput, self).__init__()
    super(QtGui.QDialog, self).__init__()
    self.setupUi(self)
    self.btnChange.clicked.connect(self.passwordChangeClicked)

  def passwordChangeClicked(self):
    return self.done(1)

  def getValue(self):
    return self.txtPassword.text()