# Name: get_time
# Function: get current system time
# Date: 2016-06-09
# Email: day9011@gmail.com
__author__ = 'day9011'
#coding=utf-8

import datetime
import time

def date2str(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")

def str2date(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    print(get_ct())
    print(get_date())
