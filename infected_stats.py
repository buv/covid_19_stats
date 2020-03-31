#!/usr/bin/env python3
import sys
import math
import pprint
import argparse
import datetime
import requests
import matplotlib.pyplot as plt

default_targets = ['France', 'Germany', 'Italy', 'Iran', 'Japan', 'Norway', 'Spain', 'Sweden', 'United Kingdom', 'US']
base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
category2filename = {
    'infected': 'time_series_covid19_confirmed_global.csv',
    'recovered': 'time_series_covid19_recovered_global.csv',
    'deaths': 'time_series_covid19_deaths_global.csv'
}

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--category", action="store", default="infected", help="Generate stats for number either of category [infected|recovered|deaths].")
parser.add_argument("-l", "--country-list", nargs='*', default=default_targets, help="List of countries/regions to analyse.")
parser.add_argument("-t", "--trigger-count", type=int, action="store", default=100, help="Case count from which to start analysis.")
args = parser.parse_args()

def get_double_time(v, days):
    # calculates the mean time for doubling for a given period or max. available data
    if len(v)<days+1:
        days = len(v)-1
    return 0. if v[-1] == v[-1-days] else days*math.log(2)/math.log(vector[-1]/vector[-1-days])

def calc_offset(v):
    # calculate offset in days based on mean increase rate of first two distinct values
    offset = 0.
    if len(v)>1:
        for idx in range(1,len(v)):
            if v[idx] > v[0]:
                offset = math.log(v[0]/args.trigger_count)/math.log(v[idx]/v[0])/idx
                break
    return offset

#
# main
#
req = requests.get(base_url+category2filename[args.category])
if req.status_code != requests.codes.ok:
    print('Content was not found.')
    sys.exit()

ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
data = {}
# aggregate regions first
for line in req.text.split('\n'):
    if not line:
        continue
    region, country, lat, lon, *cases = line.split(',')
    if country in args.country_list:
        if country in data:
            data[country] = [ data[country][idx]+int(cases[idx]) for idx in range(len(cases)) ]
        else:
            data[country] = [ int(v) for v in cases ]
# truncate data below trigger
skip_country = []
for country, cases in data.items():
    if data[country][-1] < args.trigger_count:
        skip_country.append(country)
    for idx, value in enumerate(cases):
        if int(value) > args.trigger_count:
            data[country] = [ v for v in cases[idx:] ]
            break

print("Times to double number of {} people in days".format(args.category))
print("=================================================")
print("                  {}".format(ts))
print("                  last day and last week average")
print("Country           1-day  7-days")
print("-------------------------------")
for country, vector in sorted(data.items()):
    if len(vector)>1 and country not in skip_country:
        print("{:15s}:  {:5.2f}  {:5.2f}".format(country, get_double_time(vector, 1), get_double_time(vector, 7)))
        # normalize starting point by creating an x-axis offset
        # this offset is calculated from the derivative of the first point above trigger_count
        plt.plot([ i+calc_offset(vector) for i in range(len(vector)) ], vector, label=country)

plt.gca().set_yscale('log')
plt.legend(loc='best')
plt.xlabel("days since {} {}".format(args.trigger_count, args.category))
plt.ylabel("# {}".format(args.category))
plt.title("Corona {} ({})".format(args.category, ts))
plt.grid(b=True, which='major', linestyle='--')
plt.grid(b=True, which='minor', linestyle='--', alpha=0.2)
plt.show()    
