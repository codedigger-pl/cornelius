# -*- coding: utf-8 -*-

###############################################################################
# settings.py
#
# author: Paweł Surowiec (codedigger)
# creation date: 12.05.2014
# version: 0.0.1
#
# Module contains default values for connection with database
###############################################################################

SETTINGS_PY_VERSION=(0,0,1)

#-------------------------------------------------------------- database sttings
db_userName='cornelius'
db_userPassword='cornelius'
db_host='localhost'
db_port='5432'
db_name='cornelius'
db_driver='postgres'

db_string=db_driver+'://'+                                                    \
  db_userName+':'+db_userPassword+'@'+                                        \
  db_host+':'+db_port+'/'+                                                    \
  db_name

# Do we have to create tables? Set this to true before first system start.
# After this, set this to false, or all your data will be lost.
db_createTables=False