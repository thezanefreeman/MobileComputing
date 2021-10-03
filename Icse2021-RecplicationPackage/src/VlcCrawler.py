import json
from datetime import datetime
from json.decoder import JSONDecodeError
from multiprocessing.pool import ThreadPool

import pandas as pd
import requests
from tqdm import tqdm

import Constants as Const
import DataLoader

ENDPOINT = 'https://trac.videolan.org/vlc/jsonrpc'
DATE_TIME_FORMAT = r"%Y-%m-%dT%H:%M:%S"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    # 'Content-Type': 'application/json'
}

requestBodyForQuery = {
    "params": ["max=0"],
    "method": "ticket.query"
}


def requestBodyForGetIssue(issue_id):
    return {
        "params": [issue_id],
        "method": "ticket.get",
        "max": 0
    }


response = requests.post(ENDPOINT, headers=HEADERS, json=requestBodyForQuery)
response_text = response.text
issue_ids = json.loads(response_text)['result']


def get_issue(issue_id):
    try:
        issue_response = requests.post(
            ENDPOINT,
            headers=HEADERS,
            json=requestBodyForGetIssue(issue_id))
        issue_text = issue_response.text
        issue = json.loads(issue_text)['result'][3]
        issue['time'] = datetime.strptime(
            issue['time']['__jsonclass__'][1], DATE_TIME_FORMAT)
        issue['changetime'] = datetime.strptime(
            issue['changetime']['__jsonclass__'][1], DATE_TIME_FORMAT)
        issue['id'] = issue_id
        return issue
    except Exception as e:
        print(f'Could not get issue_id: {issue_id}')
        return False


with ThreadPool(processes=32) as pool:
    issues = list(tqdm(pool.imap(get_issue, issue_ids),
                       total=len(issue_ids)))

issues = list(filter(lambda x: x, issues))
print(f'\nCrawled {len(issues)} issues')

df = pd.DataFrame(issues)

relevant_vlc_issues = df[df['platform'].str.contains('Android') & (df['type']=='defect')]

DataLoader.save_df_compressed(Const.VLC_ISSUES, relevant_vlc_issues)