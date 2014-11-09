# -*- coding: utf-8 -*-

###############################################################################
# db.py
#
# author: Paweł Surowiec (codedigger)
# creation date: 12.05.2014
# version: 0.0.1
#
# Module contains default classes for working with database - PostgreSQL. See
# settings.py in this package for configurations (connection, username, etc.).
# Rememeber to set db_createTables to False after first start.
#
# Calling this module directly, it will set db_createTables to True and reset
# all tables
###############################################################################

DB_PY_VERSION=(0,0,1)

from sqlalchemy import (create_engine, Column, ForeignKey,
                        Integer, String, Boolean, DateTime, LargeBinary )
from sqlalchemy.orm import sessionmaker, relationship, backref, relation
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
from db import settings

# Some base database settings
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
  """Check, if given login is free

  input: login - String with login name
  output: boolean valu - true if login name is free, false otherwise"""
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
class Integra(Base):
  """Satel Integra systems

  relations:
      OneToMany with Detector
      OneToMany with Zone
      OneToMany with Out"""
  __tablename__='integra'
  id=Column(Integer, primary_key=True)

  name=Column(String(25))

  detectors=relationship('Detector')
  zones=relationship('Zone')
  outs=relationship('Out')

class Detector(Base):
  """Detectors in any system

  relations:
      ManyToOne from Integra"""
  __tablename__='detectors'
  id=Column(Integer, primary_key=True)

  name=Column(String(25))

  # In which system is this detector
  system=Column(Integer, ForeignKey('integra.id'))

class Zone(Base):
  """Zones in any system. Zones has some detectors, but we don't use this
  at this moment

  relations:
      ManyToOne from Integra"""
  __tablename__='zones'
  id=Column(Integer, primary_key=True)

  name=Column(String(50))

  # in which system is this zone
  system=Column(Integer, ForeignKey('integra.id'))

class Out(Base):
  """Outs in any system

  relations:
      ManyToOne from Integra"""
  __tablename__='outs'
  id=Column(Integer, primary_key=True)

  name=Column(String(50))

  # in which system is this zone
  system=Column(Integer, ForeignKey('integra.id'))

#------------------------------------------------------------------------------
class DetectorPoint(Base):
  """Cennecting Detectors from system to map with some point

  relations:
      ManyToOne with Detector
      ManyToOne from Map"""
  __tablename__='detectorPoints'
  id=Column(Integer, primary_key=True)

  pointX=Column(Integer)
  pointY=Column(Integer)

  detectorID=Column(Integer, ForeignKey('detectors.id'))
  detector=relationship('Detector')

  map=Column(Integer, ForeignKey('maps.id'))

class ZonePoint(Base):
  """Connecting Zones from system to map with some points

  relations:
      ManyToOne with Zone
      ManyToOne from Map"""
  __tablename__='zonePoints'
  id=Column(Integer, primary_key=True)

  pointsX=Column(ARRAY(Integer))
  pointsY=Column(ARRAY(Integer))

  zoneID=Column(Integer, ForeignKey('zones.id'))
  zone=relationship('Zone')

  map=Column(Integer, ForeignKey('maps.id'))

class OutPoint(Base):
  """Connect outs from system to map with some point

  relations:
      ManyToOne with Out
      ManyToOne from Map"""
  __tablename__='outPoints'
  id=Column(Integer, primary_key=True)

  pointX=Column(Integer)
  pointY=Column(Integer)

  outID=Column(Integer, ForeignKey('outs.id'))
  out=relationship('Out')

  map=Column(Integer, ForeignKey('maps.id'))

class Map(Base):
  """Maps in Cornelius system

  relations:
      OneToMany with DetectorsPoints
      OneToMany with ZonesPoints
      OneToMany with OutsPoints"""
  __tablename__='maps'
  id=Column(Integer, primary_key=True)

  name=Column(String(50))
  graphic=Column(LargeBinary)

  detectors=relationship('DetectorPoint')
  zones=relationship('ZonePoint')
  outs=relationship('OutPoint')
#------------------------------------------------------------------------------

#-------------------------------------------------------------------------- main
# If called as app, reset database
#TODO: Fix this
if __name__ == '__main__':
  settings.db_createTables=True


# Creating initial database with default values. If there are some data,
# reseting whole database
if settings.db_createTables:

  # Creating tables
  Base.metadata.drop_all(engine)
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