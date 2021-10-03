import numpy as np

import Constants as Const
import DataLoader

firefox_issues = DataLoader.load_df_compressed(Const.FIREFOX_ISSUES_ANDROID)
vlc_issues = DataLoader.load_df_compressed(Const.VLC_ISSUES)
signal_issues = DataLoader.load_df_compressed(Const.SIGNAL_ISSUES)
nextcloud_issues = DataLoader.load_df_compressed(Const.NEXTCLOUD_ISSUES)


firefox_times = (firefox_issues['creation_time'].min(), firefox_issues['creation_time'].max())
vlc_times = (vlc_issues['time'].min(), vlc_issues['time'].max())
signal_times = (signal_issues['created_at'].min(), signal_issues['created_at'].max())
nextcloud_times = (nextcloud_issues['created_at'].min(), nextcloud_issues['created_at'].max())

print(f'firefox issues: {len(firefox_issues)} from {firefox_times[0]} to {firefox_times[1]}')
print(f'vlc issues: {len(vlc_issues)} from {vlc_times[0]} to {vlc_times[1]}')
print(f'signal issues: {len(signal_issues)} from {signal_times[0]} to {signal_times[1]}')
print(f'nextcloud issues: {len(nextcloud_issues)} from {nextcloud_times[0]} to {nextcloud_times[1]}')

print()
reviews = DataLoader.load_df_compressed(Const.APP_REVIEWS)

review_times = reviews.groupby('app_id').agg({
    "at" : [np.min,np.max]
    })

print(review_times)

firefox_reviews = reviews[reviews['app_id']==Const.FIREFOX_ID]
vlc_reviews = reviews[reviews['app_id']==Const.VLC_ID]
signal_reviews = reviews[reviews['app_id']==Const.SIGNAL_ID]
nextcloud_reviews = reviews[reviews['app_id']==Const.NEXTCLOUD_ID]

print(f'firefox reviews: {len(firefox_reviews)}')
print(f'vlc reviews: {len(vlc_reviews)}')
print(f'signal reviews: {len(signal_reviews)}')
print(f'nextcloud reviews: {len(nextcloud_reviews)}')
print()





firefox_problem_reviews = firefox_reviews[firefox_reviews['review_class']=='bug_report']
vlc_problem_reviews = vlc_reviews[vlc_reviews['review_class']=='bug_report']
signal_problem_reviews = signal_reviews[signal_reviews['review_class']=='bug_report']
nextcloud_problem_reviews = nextcloud_reviews[nextcloud_reviews['review_class']=='bug_report']

print(f'firefox problem reviews: {len(firefox_problem_reviews)}')
print(f'vlc problem reviews: {len(vlc_problem_reviews)}')
print(f'signal problem reviews: {len(signal_problem_reviews)}')
print(f'nextcloud problem reviews: {len(nextcloud_problem_reviews)}')
print()