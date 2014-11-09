'''
Created on 12 wrz 2014

@author: codedigger
'''

#---------------------------------------------- Ustawienia dotyczące bazy danych
db_userName='integrate'
db_userPassword='integrate'
db_host='localhost'
db_port='5432'
db_name='cornelius'
db_driver='postgres'

db_string=db_driver+'://'+                                                    \
  db_userName+':'+db_userPassword+'@'+                                        \
  db_host+':'+db_port+'/'+                                                    \
  db_name

# Tworzenie tabel - ustawić na True przy pierwszym uruchomieniu
db_createTables=True