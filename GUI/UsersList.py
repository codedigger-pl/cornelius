from PyQt4 import QtCore, QtGui
from QtD import UI_UsersList
from db import db
from GUI.DlgPasswordInput import DlgPasswordInput
from GUI.DlgUserAdd import DlgUserAdd

class UsersList(UI_UsersList.Ui_Uzytkownicy, QtGui.QDockWidget):
  def __init__(self):
    super(UsersList, self).__init__()
    self.setupUi(self)
    self.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
    self.btnUserPassChange.clicked.connect(self.userPasswordChangeClicked)
    self.btnUserAdd.clicked.connect(self.userAddClicked)

  def loadData(self):
    self.tblUsers.clearContents()
    session=db.Session()
    users=session.query(db.User).all()
    self.tblUsers.setRowCount(len(users))
    for row, user in enumerate(users):
      self.tblUsers.setItem(row,0,QtGui.QTableWidgetItem(user.login))
      self.tblUsers.setItem(row,1,QtGui.QTableWidgetItem(user.firstName))
      self.tblUsers.setItem(row,2,QtGui.QTableWidgetItem(user.lastName))
      chkBoxItem=QtGui.QTableWidgetItem()
#       chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      if user.isAdmin: chkBoxItem.setCheckState(QtCore.Qt.Checked)
      else: chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
      self.tblUsers.setItem(row,3, chkBoxItem)

  def userPasswordChangeClicked(self):
    newPassDialog=DlgPasswordInput()
    if newPassDialog.exec():
      selectedUserLogin=self.tblUsers.selectedItems()[0].text()
      session=db.Session()
      user=session.query(db.User).filter(db.User.login==selectedUserLogin).first()
      session.add(user)
      user.password=user.encryptPassword(newPassDialog.getValue())
      session.commit()

  def userAddClicked(self):
    userAddDialog=DlgUserAdd()
    if userAddDialog.exec()!=0:
      session=db.Session()
      user=db.User()
      session.add(user)
      user.login=userAddDialog.getLogin()
      user.firstName=userAddDialog.getFirstName()
      user.lastName=userAddDialog.getLastName()
      user.isAdmin=userAddDialog.getIsAdmin()
      user.password=user.encryptPassword(userAddDialog.getPassword())
      session.commit()
      self.loadData()