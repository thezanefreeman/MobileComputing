import pandas as pd
from google_play_scraper import Sort, reviews

import Constants as Const
import DataLoader


def get_reviews(app_id, count=10_000):
    app_reviews, _ = reviews(
        app_id,
        lang='en',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.MOST_RELEVANT,  # defaults to Sort.MOST_RELEVANT
        count=count,  # defaults to 100
        filter_score_with=None
    )

    for r in app_reviews:
        r['app_id'] = app_id
    
    return app_reviews

# firefox_reviews = get_reviews(Const.FIREFOX_ID)
# vlc_reviews = get_reviews(Const.VLC_ID)
# signal_reviews = get_reviews(Const.SIGNAL_ID)
nextcloud_reviews = get_reviews(Const.NEXTCLOUD_ID)


# app_reviews = firefox_reviews + vlc_reviews + signal_reviews

df = pd.DataFrame(nextcloud_reviews)
DataLoader.save_df_compressed(Const.NEXTCLOUD_REVIEWS, df)
print(df)

# DataLoader.save_df_compressed(Const.APP_REVIEWS, df)
