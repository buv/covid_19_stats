#!/usr/bin/env python3
import sys
import math
import pprint
import argparse
import datetime
import requests
import urllib.parse
import matplotlib.pyplot as plt

default_targets = ['France', 'Germany', 'Italy', 'Iran', 'Japan', 'Norway', 'Spain', 'Sweden', 'United Kingdom', 'US']
github_repo = 'CSSEGISandData/COVID-19'
github_path = 'csse_covid_19_data/csse_covid_19_time_series/'
category2filename = {
    'infected': 'time_series_covid19_confirmed_global.csv',
    'recovered': 'time_series_covid19_recovered_global.csv',
    'deaths': 'time_series_covid19_deaths_global.csv'
}

co = ''
parser = argparse.ArgumentParser(description='Read current covid-19 data from Johns Hopkins University, select countries of interest, compare countries course by shifting corresponding curve to a virtual outbreak date.')
group = parser.add_mutually_exclusive_group()
group.add_argument("-i", "--infected", action="store_const", const="infected", dest="category", default="infected", help="Generate stats for infected (default).")
group.add_argument("-r", "--recovered", action="store_const", const="recovered", dest="category", help="Generate stats for recovered.")
group.add_argument("-d", "--deaths", action="store_const", const="deaths", dest="category", help="Generate stats for deaths.")
parser.add_argument("-l", "--country-list", nargs='*', default=default_targets, help="List of countries/regions to analyse.")
parser.add_argument("-t", "--trigger-count", type=int, action="store", default=100, help="Case count from which to start analysis.")
args = parser.parse_args()

def get_double_time(v, days):
    # calculates the mean time for doubling for a given period or max. available data
    double_time = 0.
    if len(v) > 1:
        if len(v) < days+1:
            days = len(v)-1
        for idx in range(-1-days, -len(v), -1):
            if v[-1] > v[idx]:
                double_time = (-1-idx)*math.log(2)/math.log(vector[-1]/vector[idx])
                break
        return double_time

def calc_offset(v):
    # calculate offset in days based on mean increase rate of first two distinct values
    offset = 0.
    if len(v) > 1:
        for idx in range(1,len(v)):
            if v[idx] > v[0]:
                offset = math.log(v[0]/args.trigger_count)/math.log(v[idx]/v[0])/idx
                break
    return offset

#
# main
#
github_filename = github_path+category2filename[args.category]
req = requests.get('https://api.github.com/repos/{}/commits?path={}&page=1&per_page=1'.format(github_repo, urllib.parse.quote(github_filename, safe='')))
if req.status_code == requests.codes.ok:
    ts = req.json()[0]['commit']['committer']['date']
else:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

req = requests.get('https://raw.githubusercontent.com/{}/master/{}'.format(github_repo, github_filename))
if req.status_code != requests.codes.ok:
    print('Content was not found.')
    sys.exit()

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

title = "Times to double number of {} in days".format(args.category)
print(title)
print("="*len(title))
print("(Johns Hopkins University data from {})".format(ts))
print("                  last day and last week average")
print("Country           1-day  7-days")
print("-------------------------------")
for country, vector in sorted(data.items()):
    if len(vector) > 1 and country not in skip_country:
        print("{:15s}:  {:5.2f}  {:5.2f}".format(country, get_double_time(vector, 1), get_double_time(vector, 7)))
        # normalize starting point by creating an x-axis offset
        # this offset is calculated from the derivative of the first point above trigger_count
        plt.plot([ i+calc_offset(vector) for i in range(len(vector)) ], vector, label=country)

plt.gca().set_yscale('log')
plt.legend(loc='best')
plt.xlabel("days since {} {}".format(args.trigger_count, args.category))
plt.ylabel("# {}".format(args.category))
plt.title("COVID-19 {}\n(Johns Hopkins University data from {})".format(args.category, ts))
plt.grid(b=True, which='major', linestyle='--')
plt.grid(b=True, which='minor', linestyle='--', alpha=0.2)
plt.show()    
