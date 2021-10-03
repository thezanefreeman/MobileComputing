import logging
import pickle

import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials

from Constants import *

logger = logging.getLogger(__file__)
logger.setLevel(level=logging.INFO)


def load_df_compressed(file):
    return pd.read_csv(file, compression='gzip')


def save_df_compressed(file, df):
    return df.to_csv(file, compression='gzip', index=False)


def load_embeddings(file):
    try:
        with open(file, 'rb') as f:
            embeddings = pickle.load(f)
            logger.info(f'embeddings loaded from: {file}')
            return embeddings
    except FileNotFoundError:
        logger.info(f'embeddings file not found at: {file}')
        return {}


def save_embeddings(file, embeddings):
    with open(file, 'wb') as f:
        pickle.dump(embeddings, f, pickle.HIGHEST_PROTOCOL)
        logger.info(
            f'stored embeddings to {file}')

def load_resolved_sheet() -> pd.DataFrame:

    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    gc = gspread.authorize(credentials)
    wb = gc.open_by_key(FILE_NAME)
    sheet = wb.worksheet(SHEET_NAME)
    df = pd.DataFrame(sheet.get_all_records())

    df['relevant_review'] = df['relevant_review'].apply(lambda x: x=='TRUE')
    df['fitting_issue'] = df['fitting_issue'].apply(lambda x: x=='TRUE')
    df['searched_manually'] = df['searched_manually'].apply(lambda x: x=='TRUE')
    df['found_relevant_issue_manually'] = df['found_relevant_issue_manually'].apply(lambda x: x=='TRUE')
    df.replace({
        FIREFOX_ID: 'Firefox',
        VLC_ID: 'VLC',
        SIGNAL_ID: 'Signal',
        NEXTCLOUD_ID: 'Nextcloud'

    }, inplace=True)
    df.rename(
        columns={
            "distance": "Similarity",
            "app": "App",
            "fitting_issue": "Matching Bug Report"
            }, inplace=True)

    return df


if __name__ == "__main__":
    print(load_resolved_sheet())
