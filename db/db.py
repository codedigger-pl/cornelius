# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
from db import settings
from statics import statics

engine=create_engine(settings.db_string, echo=False)
Session=sessionmaker(bind=engine)

Base=declarative_base()

class User(Base):
  """User information"""
  __tablename__='users'
  id=Column(Integer, primary_key=True)
  login=Column(String)
  firstName=Column(String)
  lastName=Column(String)
  password=Column(String)
  isAdmin=Column(Boolean)

  def __init__(self):
    super(User, self).__init__()

  def __repr__(self):
    return '<User(login="%s", firstName="%s", lastName="%s", password="%s")>' % (self.login, self.firstName, self.lastName, self.password)

  def encryptPassword(self, password):
    """Generate encrypted password

    input: password - String: unencrypted password in plain text
    output: encrypted password with brypt library"""
    return bcrypt.hashpw(password, bcrypt.gensalt())

  def isPasswordCorrect(self, password):
    """Check, if password for this user is correct

    input: password - String: encrypted by bcrypt library password
    output: boolean value, true if password is correct, false otherwise"""
    if bcrypt.hashpw(password, self.password)==self.password: return True
    else: return False

def isLoginFree(login):
  """Check, if login is free"""
  session=Session()
  if session.query(User.login).filter(User.login==login).count==0:
    session.close()
    return True
  else:
    session.close()
    return False
#------------------------------------------------------------------------------

class AlarmReason(Base):
  """Alarm reasons, table for data from GUI.DlgAlarmConfirmation"""
  __tablename__='alarmReasons'
  id=Column(Integer, primary_key=True)
  reason=Column(String)

  def __init__(self, reason):
    super(AlarmReason, self).__init__()
    self.reason=reason

class AlarmReasons:
  """Default data for alarm reasons"""
  systemCheck=1
  falseAlarm=2
  breakeIn=3
  userError=4
  systemError=5

#------------------------------------------------------------------------------

class AlarmAction(Base):
  """Reactions, table for data from GUI.DlgAlarmConfirmation"""
  __tablename__='alarmActions'
  id=Column(Integer, primary_key=True)
  action=Column(String)

  def __init__(self, action=''):
    super(AlarmAction, self).__init__()
    self.action=action

class AlarmActions:
  """Defaults data for alarm actions (reactions)"""
  sentPatrol=1
  notifiedGroup=2
  notifiedOD=3
  notifiedAdministrator=4
  notifiedKO=5
#------------------------------------------------------------------------------

# actions=Table('actions', Base.metadata,
#               Column('alarmAction_id', Integer, ForeignKey('alarm_actions.id')),
#               Column('alarmEvent_id', Integer, ForeignKey('alarm_events.id')))

class AlarmEvent(Base):
  """Events registry from systems"""
  __tablename__='alarmEvents'
  id=Column(Integer, primary_key=True)

  # user accepted event
  confirmUserID=Column(Integer, ForeignKey('users.id'))
  confirmUser=relationship('User', backref=backref('events', order_by=id))

  # Event date and time
  date=Column(DateTime)

  # Name of zone
  zoneName=Column(String)

  # Alarm type
  alarmType=Column(String)

  # Detectors
  detectors=Column(ARRAY(String))

  # comment for event
  comment=Column(String)

  # Alarm reason
  reasonID=Column(Integer, ForeignKey('alarmReasons.id'))
  reason=relationship('AlarmReason', backref=backref('alarmReasons'))

  # Actions made by user, Seems, like SQLAlchemy don't support foreign key in
  # PostgreSQL ARRAY's. But in this way we can see, what is in this field
  actions=Column(ARRAY(Integer, ForeignKey('alarmActions.id')))
#   actions=relationship('AlarmAction', secondary=actions, backref='alarm_events')

#------------------------------------------------------------------------------


if settings.db_createTables:
  Base.metadata.create_all(engine)
  session=Session()

  # Adding default user: admin/admin
  user=User()
  user.login='admin'
  user.firstName='Admin'
  user.lastName='Administrator'
  user.password='$2a$12$.Sj0qhhdWi9XZ6m0TJXmXOkq2p4jcGocBhntcIyhzqKZriRIZIvOa'
  user.isAdmin=True
  session.add(user)

  # Creating default AlarmReasons
  session.add(AlarmReason('Sprawdzenie systemu'))
  session.add(AlarmReason('Fałszywy alarm'))
  session.add(AlarmReason('Włamanie do strefy'))
  session.add(AlarmReason('Błąd użytkownika'))
  session.add(AlarmReason('Błąd systemu'))

  # Creating default AlarmActions
  session.add(AlarmAction('Wysłano patrol'))
  session.add(AlarmAction('Wezwano grupę interwencyjną'))
  session.add(AlarmAction('Powiadomiono Oficera Dyżurnego'))
  session.add(AlarmAction('Powiadomiono Administratora'))
  session.add(AlarmAction('Powiadomiono Komendanta Ochrony'))

  session.commit()

if __name__ == '__main__':
    pass