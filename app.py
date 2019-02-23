import pandas as pd
import datetime
import matplotlib as plt

import csv

with open('test.csv', 'r') as f:
    reader = csv.reader(f, delimiter='|')
    headers = next(reader, None)
    column = {}

    for h in headers:
        column[h] = []

    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)


list_date = pd.to_datetime(column['created_at'])

dates = {}
for date in list_date:
    date = date.replace(microsecond=0,second=0,minute=0)
    if date in dates:
        dates[date] += 1
    else:
        dates[date] = 1

data_set = pd.DataFrame.from_dict(dates, orient="index")

data_set.plot()
# max_date = max(list_date).replace(microsecond=0,second=0,minute=0)
# min_date = min(list_date).replace(microsecond=0,second=0,minute=0)
#
# print(pd.date_range(min_date, max_date, freq="H"))


