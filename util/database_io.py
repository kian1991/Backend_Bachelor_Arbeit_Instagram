from util.instagram import ClientError, instagram_client
from util.StoreNewAccountThread import StoreNewAccountThread
from util.database import db

# Globals
STORETHREAD = None  # In dieser Variable wird der Thread zur Speicherung der neuen Accountdaten gespeichert


def get_available_data(username, limit):
    global STORETHREAD
    try:
        user_info = instagram_client.username_info(username)
        '''
            Prüfen ob User bereits in der Datenbank vorhanden ist, falls in der Datenbank ein Eintrag vorhanden ist wird es 
            in entry gespeichert. Andernfalls ist entry = None.
            Falls ein limit Festgelegt wurde wird nur ein teil der in dem Usereintrag einthaltenen Medien übertragen.
        '''
        entry = db['users'].find_one({'username': username})
        if entry:
            if limit:
               entry['media'] = entry['media'][0:limit]
            return entry, True  # Aus Datenbank lesen todo
        else:
            if not STORETHREAD or not STORETHREAD.isAlive():
                STORETHREAD = StoreNewAccountThread(user_info['user']['pk'])
                STORETHREAD.start()
            return user_info, False
    except ClientError as e:
        return {'error': str(e)}, False
