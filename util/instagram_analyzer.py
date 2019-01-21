import re
from collections import Counter
'''
    Dieses Modul nimmt einen die Medien eines Datensatz, in der für die Datenbank festgelegten Datenstuktur, 
    entgegen berechnet die Festgelegten Kennzahlen und Metriken
'''



'''
    @:return Hashtagliste mit den sortierten Tags
'''
def calculate_engagement_extract_hashtags(media, follower_count):
    hashtags = []
    for media_entry in media:
        # Die Hashtags mittels einer Regular Expression herausfiltern, bietet sich hier an, da bereits über
        # die Medien iteriert wird

        engagement_rate = 0

        if media_entry['caption']:
            tags_in_media = re.findall(r"#(\w+)", media_entry['caption']['text'])
            if tags_in_media:
                hashtags.extend(tags_in_media)

        if follower_count != 0:
            if media_entry['like_count']:  # Wenn likes vorhanden sind
                like_count = media_entry['like_count']
            else:
                like_count = 0

            if media_entry['comment_count']:  # Wenn kommentare vorhanden sind
                comment_count = media_entry['comment_count']
            else:
                comment_count = 0

                engagement_rate = (like_count + comment_count) / follower_count * 100

        media_entry['engagement_rate'] = engagement_rate
        continue

    return _hashtag_counter(hashtags)


def _hashtag_counter(tags):
    counted_hashtags = Counter(tags)
    sorted_and_counted_hashtags = {k: v for k, v in sorted(counted_hashtags.items(), key=lambda x: x[1], reverse=True)}
    return sorted_and_counted_hashtags
