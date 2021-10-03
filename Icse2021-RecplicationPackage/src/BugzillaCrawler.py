from __future__ import print_function

import json
import os
import time
from datetime import datetime

import pandas as pd
import requests

# relative path to data storage
DATAPATH = './data/'
FIREFOX_PRODUCTS = ['Firefox', 'Firefox for Android', 'Core']

# build query - some help for creating a query: https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html#search-bugs
# creation_time [datetime] Searches for bugs that were created at this time or later. May not be an array.
# version [string] The Version field of a bug.
# limit [int] Limit the number of results returned. If the limit is more than zero and higher than the maximum limit set by
#   the administrator, then the maximum limit will be used instead. If you set the limit equal to zero, then all matching
#   results will be returned instead.
# status [string] The current status of a bug (not including its resolution, if it has one, which is a separate field above). = "CLOSED"
# quicksearch [string] Search for bugs using quicksearch syntax.
# new_since [datetime] A datetime timestamp to only show history since.
# product=Firefox for Android
#
# Depending on the size of your query, you can massively speed things up
# by telling bugzilla to only return the fields you care about, since a
# large chunk of the return time is transmitting the extra bug data. You
# tweak this with include_fields:
# https://wiki.mozilla.org/Bugzilla:BzAPI#Field_Control
# Bugzilla will only return those fields listed in include_fields.

# bug reports initial creation datetime in iso format as string
crTimeS = '2011-01-01T00:00:00Z'
endTimeS = '2019-06-09T14:35:17Z'
datetimeFormat = '%Y-%m-%dT%H:%M:%SZ'
endTime = datetime.strptime(endTimeS, datetimeFormat)

print('Ending time for crawling bug reports:')
print(endTime)
print('Initial starting time for crawling bug reports:')
print(datetime.strptime(crTimeS, datetimeFormat))

counter = 0
totalNumberOfBugs = 0
limit = 500
resultLength = limit
isFirstRun = True

df = pd.DataFrame()
df_comments = pd.DataFrame()

while datetime.strptime(crTimeS, datetimeFormat) < endTime and resultLength == limit:
    t1 = time.time()
    query = "https://bugzilla.mozilla.org/rest/bug?product=Core&creation_time=" + crTimeS + "&limit=" + \
        str(limit) + "&include_fields=id,creation_time,last_change_time,cf_last_resolved,creator,cc,product,status,summary,severity,comments,history,component"

    tries = 50
    for i in range(tries):
        try:
            response = requests.get(query)
            t2 = time.time()

            if response.status_code != 200:
                # This means something went wrong.
                raise ApiError('GET /tasks/ {}'.format(response.status_code))

            else:
                # extract bugs and put them into a dictionary
                bugList = response.json()
                bugs = bugList["bugs"]

                resultLength = len(bugs)
                newBugs = resultLength
                lastElement = resultLength - 1
                crTimeS = bugs[lastElement]['creation_time']
                # print('Next creation_time:', crTimeS)

                # remove first element of the result set since it was included in the preceding run
                # except for the first attempt, bc there is no preceding run where a new creation_time is drawn from
                if not isFirstRun:
                    del bugs[0]
                    newBugs -= 1
                isFirstRun = False

                # deleted duplicates must be considered
                totalNumberOfBugs += newBugs

                print('Total Number of Bugs: ' + str(totalNumberOfBugs))

                df = df.append(bugs, ignore_index=True)
                for bug in bugs:
                    df_comments = df_comments.append(
                        bug['comments'], ignore_index=True)
                counter += 1
        except:
            print('Exception for crTime', crTimeS)
            if i < tries - 1:  # i is zero indexed
                continue
            else:
                raise
        break


df.to_csv('./data/df_firefox_core.csv.gzip', compression='gzip')
df_comments.to_csv(
    './data/df_firefox_core_comments.csv.gzip', compression='gzip')
