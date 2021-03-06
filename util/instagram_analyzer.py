import re
from collections import Counter
'''
    Dieses Modul nimmt einen die Medien eines Datensatz, in der für die Datenbank festgelegten Datenstuktur, 
    entgegen berechnet die Festgelegten Kennzahlen und Metriken
'''



'''
    Rückgabe ist ein objekt Array mit den extrahierten Hashtags
'''
def calculate_engagement_extract_hashtags(media, follower_count):
    hashtags = []
    for media_entry in media:
        # Die Hashtags mittels einer Regular Expression herausfiltern, 
        # bietet sich hier an, da bereits über
        # die Medien iteriert wird

        engagement_rate = 0

        if media_entry['caption']:
            tags_in_media = re.findall(r"#(\w+)", media_entry['caption']['text'])
            if tags_in_media:
                hashtags.extend(tags_in_media)

        if follower_count != 0:
            try:  # Wenn likes vorhanden sind
                like_count = media_entry['like_count']
            except KeyError:
                like_count = 0

            try:  # Wenn kommentare vorhanden sind
                comment_count = media_entry['comment_count']
            except KeyError:
                comment_count = 0

            engagement_rate = (like_count + comment_count) / follower_count * 100

        media_entry['engagement_rate'] = engagement_rate

    return __hashtag_counter(hashtags)


def __hashtag_counter(tags):
    counted_hashtags = Counter(tags)
    return counted_hashtags


