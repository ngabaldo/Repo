#!/usr/bin/python
#! src.py - A program that performs basic analytics on server log file, provides useful metrics, and implements basic security measures

import sys
from collections import OrderedDict
from time import strptime
from pytz import timezone
import re, operator, datetime, pytz

def identify_time_zone(time_zone):
    symbol = time_zone[0]
    if time_zone[1]=='0':
        meridian=time_zone[2]
    else:
        meridian = time_zone[1]+time_zone[2]
    if symbol =='-':
        new_symbol = '+'
    elif symbol == '=':
        new_symbol = '-'
    GMT_zone = 'Etc/GMT'+new_symbol+meridian
    return GMT_zone

# Read in previous transactions.
weblist = {}
resourcelist = {}
hourlist = []
times={}
IP_address_fails = {}
feature4file = open('blocked.txt','w')
errorsfile = open('errors.txt','w')
re_groups = re.compile(r'''(
[a-zA-Z0-9:._@#^&*()%+-/\?]+
)''',re.VERBOSE)
re_resource = re.compile(r'''(
".*?"
)''',re.VERBOSE)

with open('log.txt','r') as myfile:
    for line in myfile:
        try:
            #Look for regular expression.
            mo = re_groups.findall(line)
            mu = re_resource.findall(line)
            website = mo[0]
            resource_list = mu[0].split()
            resource = resource_list[1]
            #Regular expressions for Feature 1.
            try:
                weblist[website] = weblist[website]+ 1
            except KeyError:
                weblist[website] = 1
            #Regular expressions for Feature 2.
            if resource in resourcelist:
                try:
                    resourcelist[resource] = resourcelist[resource] + int(mo[-1])
                except ValueError:
                    resourcelist[resource] = resourcelist[resource] + 0
            else:
                try:
                    resourcelist[resource] = int(mo[-1])
                except ValueError:
                    resourcelist[resource] = 0
            #Regular expressions for Feature 3.
            date = mo[3].split('/')
            hour = mo[3].split(':')
            year1 = hour[0].split('/')
            year = year1[2]        
            month=strptime(date[1],'%b').tm_mon
            time_zone = mo[4]
            #Identify time zone.
            zone = identify_time_zone(time_zone)
            tzone=timezone(zone)
            date_hour=tzone.localize(datetime.datetime(int(year),int(month),int(date[0]),int(hour[1]),int(hour[2]),int(hour[3])))
            one_hour = datetime.timedelta(hours=1)
            #Count times accessed in 60 minutes window.
            if hourlist == []:
                hourlist.append([date_hour,1])
            else:
                same = 0
                for i in range(len(hourlist)):
                    if date_hour == hourlist[i][0]:
                        hourlist[i][1] = hourlist[i][1]+1
                        same = 1
                    else:
                        if date_hour-hourlist[i][0] < one_hour:
                            hourlist[i][1] = hourlist[i][1]+1
                if same == 0:
                    hourlist.append([date_hour,1])
            #For Feature 4, find in IP address is blocked or not.
            seconds20 = datetime.timedelta(seconds=20)
            minutes5 = datetime.timedelta(minutes=5)
            try:
                #Block if the same IP address has status blocked and time difference is less than 5 miuntes.
                if IP_address_fails[mo[0]][2]=='blocked':
                    if date_hour-IP_address_fails[mo[0]][3]<=minutes5:
                        feature4file.write(line)
                        feature4file.flush()
                        continue
                    else:
                        if mo[-2] == '401':
                            IP_address_fails[mo[0]][0] = date_hour
                            IP_address_fails[mo[0]][1] = 1
                            IP_address_fails[mo[0]][2] = ''
                            IP_address_fails[mo[0]][3] = ''
                            continue
                        else:
                            IP_address_fails[mo[0]][0] = date_hour
                            IP_address_fails[mo[0]][1] = 0
                            IP_address_fails[mo[0]][2] = ''
                            IP_address_fails[mo[0]][3] = ''
                            continue
                if mo[-2] == '401':
                    #Block if it is the 3rd time the same IP address fails to login
                    if date_hour-IP_address_fails[mo[0]][0]<=seconds20:
                        IP_address_fails[mo[0]][1] = IP_address_fails[mo[0]][1] +1
                        if IP_address_fails[mo[0]][1]==3:
                            IP_address_fails[mo[0]][2]='blocked'
                            IP_address_fails[mo[0]][3]=date_hour
                else:
                    if IP_address_fails[mo[0]][1]<3:
                        IP_address_fails[mo[0]][0] = date_hour
                        IP_address_fails[mo[0]][1] = 0
                        IP_address_fails[mo[0]][2] = ''
                        IP_address_fails[mo[0]][3] = ''
            except KeyError:
                    IP_address_fails[mo[0]] = [date_hour,1,'','']
        except IndexError:
            errorsfile.write('Detected a strange line in log.txt: ' + '\n'+ line)
            errorsfile.flush()
            continue
    #List in descending order the active hosts/IP addresses that have accessed the site.
    sorted_websites = sorted(weblist.items(), key=operator.itemgetter(1),reverse=True)
    sorted_websites = sorted(sorted_websites, key=lambda tup: (-tup[1], tup[0]))
    #List in descending order the resources on the site that consume the most bandwidth.
    sorted_resources= sorted(resourcelist.items(), key=operator.itemgetter(1),reverse=True)
    sorted_resources = sorted(sorted_resources, key=lambda tup: (-tup[1], tup[0]))
    #List in descending order the most active 60 minutes windows
    sorted_hours = sorted(hourlist, key=lambda x: x[1], reverse=True)
    #Print files for Features 1, 2, and 3.
    feature1file = open('hosts.txt','w')
    feature2file = open('resources.txt','w')
    feature3file = open('hours.txt','w')
    #Print Feature 1.
    for i in range(10):
        feature1file.write(sorted_websites[i][0]+','+str(sorted_websites[i][1])+'\n')
    feature1file.close()
    #Print Feature 2.
    for i in range(10):
        feature2file.write(sorted_resources[i][0]+'\n')
    feature2file.close()
    #Print Feature 3.
    for i in range(10):
        feature3file.write(sorted_hours[i][0].strftime('%d/%b/%Y:%H:%M:%S %z')+','+str(sorted_hours[i][1])+'\n')
    feature3file.close()
    feature4file.close()
    errorsfile.close()
myfile.close()
