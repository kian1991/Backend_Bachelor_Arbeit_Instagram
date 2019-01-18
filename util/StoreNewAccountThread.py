from threading import Thread
from time import sleep, time
from util.instagram import instagram_client
from util.database import db
from util.instagram_analyzer import calculate_engagement_extract_hashtags


class StoreNewAccountThread(Thread):
    def __init__(self, user_id):
        Thread.__init__(self)
        self.user_id = user_id

    def run(self):
        user = instagram_client.user_info(self.user_id)
        media = get_all_media(self.user_id)
        store_new_user(user['user'], media)




'''
    Diese Funktion splittet daten - in diesem Fall die Medien - in parts.
    Dies ist nötig da MongoDB standardgemäß ein Datengröße-Limit von 16MB hat.
'''
def chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i:i + size]


def store_new_user(user, media):

    user['_id'] = user['pk']
    user['created_at'] = int(time())
    user['follower_count_history'] = [{
        'checked_at': int(time()),
        'follower_count': user['follower_count']}]
    user['hashtags'] = calculate_engagement_extract_hashtags(media, user['follower_count'])
    '''
        Zu diesem Zeitpunkt ist der Komplette Datensatz analysiert und komplettiert. 
        Die Medien müssen vorerst wieder entfernt und dann sukzessive in die Daten Bank geschrieben werden.
        Da allerdings die Dokumentengröße 16 MB nicht übersteigen darf werden nicht mehr als 3000 einträge gespeichert
    '''
    user['media'] = media
    db['users'].insert_one(user)
    '''for chunk in chunks(media, 400):
        db['users'].update_one({'_id': user['pk']},
                           {'$addToSet': {'media':
                                              {'$each': chunk}}})'''


'''3000 Limit'''
def get_all_media(user_id, limit=None): # limit * 12 zB. 1 = 12 einträge; 2 = 24 einträge usw.
    media = []
    results = instagram_client.user_feed(user_id)
    media.extend(results.get('items', []))
    next_max_id = results.get('next_max_id')
    while next_max_id:
        successful = False
        while not successful:
            errorcount = 0
            try:
                results = instagram_client.user_feed(user_id, max_id=next_max_id)
                successful = True
            except Exception as e: # todo Fehlerbehandlung
                print(f'ERROR # {e}: Trying again')
                if 'Bad Request' in str(e):
                    print(f'ERROR # {e}: Thread will pause a minute')
                    sleep(60)
                else:
                    '''
                        An Dieser stelle werden Fehler, die beim Abrufen auftreten gezählt. 
                        Nach 5 Fehlversuchen wird der Post übersprungen
                    '''
                    errorcount += 1
                    if errorcount == 5:
                        continue
                    sleep(2)
            continue
        media.extend(results.get('items', []))
        next_max_id = results.get('next_max_id')
        if len(media) >= 3000:  # Die Abfrage wird auf 3000 Postings Limitiert.
            break
        print(next_max_id)
    return media




