# current logged user
currentLogedUser=None # db.User

# current database session
dbSession=None # db.Session()

alarmAction=('Wysłano patrol',
             'Wezwano grupę interwencyjną',
             'Powiadomiono Oficera Dyżurnego',
             'Powiadomiono Administratora',
             'Powiadomiono Komendanta Ochrony')

alarmReason=('Sprawdzenie systemu',
             'Fałszywy alarm',
             'Włamanie do strefy',
             'Błąd użytkownika',
             'Błąd systemu')

sndAlarmPath='../gfx/snd/alarm.mp3'