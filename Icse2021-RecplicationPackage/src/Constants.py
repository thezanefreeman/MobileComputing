import os

import pandas as pd

THIS_DIRECTORY = os.path.dirname(__file__)

PLOT_DIR = os.path.join(THIS_DIRECTORY,'../plots')

DATA_DIR = os.path.normpath(os.path.join(THIS_DIRECTORY, '../data/'))

APP_REVIEWS = os.path.join(DATA_DIR, 'df_app_reviews.csv.gzip')
TWEETS = os.path.join(DATA_DIR, 'df_tweets.csv.gzip')

# APP IDs
FIREFOX_ID = 'org.mozilla.firefox'
VLC_ID = 'org.videolan.vlc'
SIGNAL_ID = 'org.thoughtcrime.securesms'
NEXTCLOUD_ID = 'com.nextcloud.client'

APP_IDS = [FIREFOX_ID, VLC_ID, SIGNAL_ID, NEXTCLOUD_ID]

# App Names
FIREFOX = 'Firefox'
VLC = 'VLC'
SIGNAL = 'Signal'
NEXTCLOUD = 'Nextcloud'

APPS = [FIREFOX, VLC, SIGNAL, NEXTCLOUD]

# Firefox Issues
FIREFOX_ISSUES_ANDROID = os.path.join(
    DATA_DIR, 'df_firefox_issues_android.csv.gzip')

FIREFOX_ISSUES_ANDROID_COMMENTS = os.path.join(
    DATA_DIR, 'df_firefox_issues_android_comments.csv.gzip')

FIREFOX_ISSUES_DESKTOP = os.path.join(
    DATA_DIR, 'df_firefox_issues_desktop.csv.gzip')

FIREFOX_ISSUES_DESKTOP_COMMENTS = os.path.join(
    DATA_DIR, 'df_firefox_issues_desktop_comments.csv.gzip')

# VLC Data
VLC_ISSUES = os.path.join(
    DATA_DIR, 'df_vlc_issues.csv.gzip')

# Signal Issues
SIGNAL_REVIEWS = os.path.join(
    DATA_DIR, 'df_signal_app_reviews.csv.gzip')
SIGNAL_ISSUES = os.path.join(
    DATA_DIR, 'df_signal_issues.csv.gzip')
    
# NextCloud Issues
NEXTCLOUD_REVIEWS = os.path.join(
    DATA_DIR, 'df_nextcloud_app_reviews.csv.gzip')
NEXTCLOUD_ISSUES = os.path.join(
    DATA_DIR, 'df_nextcloud_issues.csv.gzip')

# Embedding files
FIREFOX_ANDROID_EMBEDDINGS = os.path.join(
    DATA_DIR, 'firefox_android_embeddings_nouns.pkl')

FIREFOX_EMBEDDINGS = os.path.join(
    DATA_DIR, 'firefox_embeddings_nouns.pkl')

VLC_EMBEDDINGS = os.path.join(
    DATA_DIR, 'vlc_embeddings_nouns.pkl')

SIGNAL_EMBEDDINGS = os.path.join(
    DATA_DIR, 'signal_embeddings_nouns.pkl')

NEXTCLOUD_EMBEDDINGS = os.path.join(
    DATA_DIR, 'nextcloud_embeddings_nouns.pkl')


# Annotation file
CODINGS = os.path.join(DATA_DIR, 'codings.csv')

# Google Spreadsheet
FILE_NAME = "1eDiehpGU25DcMspE1aIFfhHsKFMdgA0h5ShpPG7qUtQ"
SHEET_NAME = 'Resolved'
CREDENTIALS_FILE = os.path.join(THIS_DIRECTORY, '../credentials.json')