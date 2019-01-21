from pymongo import MongoClient

'''
Dieses Modul stellt die Datenbank dar, es bietet funktionen zur Speicherung von Instagram Accounts. 
Zudem werden Methoden bereitgestellt um gespeicherte Daten aus der Datenbank abzufragen

Folgende Collections sind angedacht:

db.user - Speicherung der Nutzerdaten
db.media - Speicherung der Veröffentlichungen
db.follower - speicherung der follower + timestamp

'''

# Client initialisieren
client = MongoClient('mongodb://naik.ml:27017/')

# Datenbank auswählen
db = client['BA_DB']




