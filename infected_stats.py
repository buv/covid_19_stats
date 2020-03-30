#!/usr/bin/env python3
import sys
import math
import pprint
import requests
import datetime
import matplotlib.pyplot as plt

trigger_count = 100.
target = ['Germany', 'Norway', 'Sweden', 'France', 'Italy', 'Spain', 'US', 'Iran', 'Japan', 'United Kingdom']
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'


def get_double_time(v, days):
    if len(v)<days-1:
        days = len(v)-1
    return 0. if v[-1] == v[-1-days] else days*math.log(2)/math.log(vector[-1]/vector[-1-days])

req = requests.get(url)
if req.status_code != requests.codes.ok:
    print('Content was not found.')
    sys.exit()

data = {}
for line in req.text.split('\n'):
    if not line:
        continue
    region, country, lat, lon, *cases = line.split(',')
    if country in target and not region:
        for idx, value in enumerate(cases):
            if int(value) > trigger_count:
                data[country] = [ int(v) for v in cases[idx:] ]
                break

print("Times to double number of infected people in days")
print("=================================================")
print("                  last day and last week average")
print("Country           1-day  7-days")
print("-------------------------------")
for country, vector in sorted(data.items()):
    print("{:15s}:  {:5.2f}  {:5.2f}".format(country, get_double_time(vector, 1), get_double_time(vector, 7)))
    offset = math.log(vector[0]/trigger_count)/math.log(vector[1]/vector[0])
    plt.plot([ i+offset for i in range(len(vector)) ], vector, label=country)

        
plt.gca().set_yscale('log')
plt.legend(loc='best')
plt.xlabel("days since {} infected".format(int(trigger_count)))
plt.ylabel("# infected")
plt.title("Corona infected ({})".format(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")))
plt.grid(b=True, which='major', linestyle='--')
plt.grid(b=True, which='minor', linestyle='--', alpha=0.2)
plt.show()    
