# covid_19_stats

This python3 script reads the covid-19 statistics from Johns Hopkins University and normalizes data to an imaginary start date where the number of infected people rises above a given threshold (e.g. 100). Furthermore the time it takes until the number of infected people doubles are calculated for the last day and the last week.

```
usage: analyize_stats.py [-h] [-i | -r | -d]
                         [-l [COUNTRY_LIST [COUNTRY_LIST ...]]]
                         [-t TRIGGER_COUNT]

Read current covid-19 data from Johns Hopkins University, select countries of
interest, compare countries course by shifting corresponding curve to a
virtual outbreak date.

optional arguments:
  -h, --help            show this help message and exit
  -i, --infected        Generate stats for infected (default).
  -r, --recovered       Generate stats for recovered.
  -d, --deaths          Generate stats for deaths.
  -l [COUNTRY_LIST [COUNTRY_LIST ...]], --country-list [COUNTRY_LIST [COUNTRY_LIST ...]]
                        List of countries/regions to analyse.
  -t TRIGGER_COUNT, --trigger-count TRIGGER_COUNT
                        Case count from which to start analysis.
```

Example to compare number of recovered cases for Germany and Italy shifting day zero to point in time when number of cases exided 200:
```
./analyize_stats.py -r -t 200 -l Italy Germany
```

Example default output:
![covid-19 stats](/example.png)

```
Times to double number of infected in days
==========================================
(Johns Hopkins University data from 2020-03-31T23:55:36Z)
                  last day and last week average
Country           1-day  7-days
-------------------------------
France         :   4.43   5.72
Germany        :   9.76   6.24
Iran           :   9.59   8.27
Italy          :  17.74  11.42
Japan          :  15.21   9.84
Norway         :  16.06  10.04
Spain          :   7.99   5.53
Sweden         :   7.20   7.32
US             :   4.59   3.87
United Kingdom :   5.48   4.26
```
