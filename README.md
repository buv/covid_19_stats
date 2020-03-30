# covid_19_stats

This python3 script reads the covid-19 statistics from Johns Hopkins University and normalizes data to an imaginary start date where the number of infected people rises above a given threshold (e.g. 100). Furthermore the time it takes until the number of infected people doubles are calculated for the last day and the last week.

Example output:
![covid-19 stats](/example.png)

```
Times to double number of infected people in days
=================================================
                  2020-03-30 23:21:50 UTC
                  last day and last week average
Country           1-day  7-days
-------------------------------
France         :  10.36   5.28
Germany        :   9.43   5.30
Iran           :   8.80   8.49
Italy          :  12.63   9.67
Japan          :   7.12   9.20
Norway         :  10.69   8.28
Spain          :   7.73   4.74
Sweden         :   9.79   7.48
US             :   4.68   3.36
United Kingdom :   5.21   3.93
```
