from util.database import db
from time import time, sleep
from util.instagram import instagram_client
from util.instagram_analyzer import calculate_engagement_extract_hashtags

'''
    Description
'''

# Der Prozess soll alle 10 Minuten anfangen, die Datenbank aufzufrischen
update_interval = 60 * 10


def check__database_accounts():
    print('checking')
    # Alle Accounts aus der Datenbank abrufen
    cursor = db['users'].find()
    # Über den Cursor iterieren
    for account in cursor:
        print('Updating Information: ' + account['username'])
        try:
            # aktuelle Profildaten abrufen und mit DB-Eintrag vergleichen
            current_info = instagram_client.user_info(account['pk'])['user']
            # Die Filter Query initialisieren
            filter = {'_id': account['pk']}

            # Abonnentenzahlen
            if account['follower_count'] != current_info['follower_count']:
                new_history_entry = {
                    'checked_at': int(time()),
                    'follower_count': current_info['follower_count']
                }
                db['users'].update_one(filter, {'$push': {'follower_count_history': new_history_entry}})

            # Medien
            if account['media_count'] != current_info['media_count']:
                new_media = instagram_client.user_feed(account['pk'])['items']
                # nur neue Einträge herausfiltern, das Veröffentlichungsdatum wird mit dem, der neusten Veröffentlichung
                # in der Datenbank verglichen.
                new_media = [m for m in new_media if m['taken_at'] > account['media'][0]['taken_at']]
                # Die Daten mit den aktuellen Abonnentenzahlen analysieren
                new_hashtags = calculate_engagement_extract_hashtags(new_media, current_info['follower_count'])
                # Die neuen Hashtags zu den alten hinzu addieren hinzufügen
                old_tags = account['hashtags']
                for tag, count in new_hashtags.items():
                    if tag in old_tags:
                        old_tags[tag] += count
                    else:
                        old_tags[tag] = count

                db['users'].update_one(filter, {'$push': {'media': {'$each': new_media, '$position': 0}}})
                db['users'].update_one(filter, {'$set': {'hashtags': new_hashtags}})



            db['users'].update_one(filter, {'$set': current_info})

        except Exception as e:
            print('ERROR:' + str(e))


if __name__ == '__main__':

    while True:
        check__database_accounts()
        sleep(update_interval)



