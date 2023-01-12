#!/usr/bin/env python3
from checks import AgentCheck
import datetime
import os
from datetime import timedelta

# Path to the file
path = r"/etc/datadog-agent/checks.d/raidwear.txt"

# file modification timestamp of a file
m_time = os.path.getmtime(path)
# convert timestamp into DateTime object
dt_m = datetime.datetime.fromtimestamp(m_time).strftime('%Y-%m-%d %H:%M:%S')

#get last hour for comparison.
from datetime import datetime, timedelta
last_hour_date_time = datetime.now() - timedelta(hours = 1)
dt_lh = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

#return true if file date/time > current date/time - 1 hour
def compare_dates(date1, date2):
    # convert string to date
    dt_obj1 = str(datetime.strptime(date1, "%Y-%m-%d %H:%M:%S"))
    dt_obj2 = str(datetime.strptime(date2, "%Y-%m-%d %H:%M:%S"))

    if dt_obj1 == dt_obj2:
        return('')
    elif dt_obj1 > dt_obj2:
        return('true')
    else:
        return('false')

#datetime in yyyy-mm-dd hh:mm:ss format. setting flag to ensure raidwear.txt modified date > current time - 1 hour
fileuptodate_flag = str(compare_dates(dt_m, dt_lh))

#Sending raid wear level metric to datadog
class RaidWearCheck(AgentCheck):
  def check(self, instance): 
    # Using readlines()
    file1 = open('/etc/datadog-agent/checks.d/raidwear.txt', 'r')
    Lines = file1.readlines()
    
    #variable used to identify key and value
    spl_char = ':'
    count = 0
    #loop and extract disk and associated wear level count value
    for line in Lines:
        count += 1
        if line != '':
            value=line.strip() 
        
        if value != '':
            #partition() to get disk
            diskraid = str(value).partition(spl_char)[0]
            #split to get wear level count value
            wear_lvl=str(value.split(spl_char,1)[1])
            if fileuptodate_flag == 'true':
                #changing wear level count value to int() as it is a datadog requirement for gauge type metric
                wear = int(wear_lvl) 
            else:
                wear = 0
            #sending the metric to datadog as metric ex: disk0.wear.level
            self.gauge(diskraid+'.wear.level', wear)
