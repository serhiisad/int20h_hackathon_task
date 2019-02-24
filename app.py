"""
Spyder Editor

"""

import pandas as pd
import numpy
import glob
import datetime
from statsmodels.tsa.arima_model import ARIMA
import json
import ntpath

def difference(dataset, interval=1):
  diff = list()
  for i in range(interval, len(dataset)):
    value = dataset[i] - dataset[i - interval]
    diff.append(value)
  return numpy.array(diff)

def inverse_difference(history, yhat, interval=1):
  return yhat + history[-interval]

def create_week(start_date):
    start_datetime = datetime.datetime.strptime(start_date.split('.')[0], '%Y-%m-%d %H:%M:%S')
    week = []
    for i in range(168):
        start_datetime += datetime.timedelta(hours=1)
        week.append(start_datetime.strftime('%Y-%m-%d %H:%M:%S'))
    return week

path = 'conf_data/clusters/*.json'

files=glob.glob(path)

a = 0
for file in files:
    dates = {}
    with open(file, 'r') as f:
        string = f.read()
        data = json.loads(string)
        
        for date in data:
            ddate = pd.to_datetime(date).replace(microsecond=0, second=0, minute=0)
            if ddate in dates:
                dates[ddate] += 1
            else:
                dates[ddate] = 1
    
    data_set = pd.DataFrame.from_dict(dates, orient="index")
    data_set.plot(figsize=(20, 10))
    # load dataset
    series = data_set
    # seasonal difference
    X = series.values

    try:
        days_in_year = 365
        differenced = difference(X, days_in_year)
        # fit model
        model = ARIMA(differenced, order=(7,0,1))
        model_fit = model.fit(disp=0)
        # multi-step out-of-sample forecast
        start_index = len(differenced)
        end_index = start_index + 6
        forecast = model_fit.predict(start=start_index, end=end_index)
        # invert the differenced forecast to something usable
        history = [x for x in X]
        day = 1
        for yhat in forecast:
        	inverted = inverse_difference(history, yhat, days_in_year)
        	print('Day %d: %f' % (day, inverted))
        	history.append(inverted)
        	day += 1
        
        f = open('new_'+ ntpath.basename(file), 'w')
        f.write(json.dumps(history))
        
    except Exception as e:
         print(file)
         print(e)
         
    a += 1
