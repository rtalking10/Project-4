#Imports the different functions as needed
from os.path import exists as exist
from datetime import datetime
import re

#Creates a local copy of the log if it doesn't already exist
if not exist('local_copy.log'):
    from urllib.request import urlretrieve
    URL_PATH = 'https://s3.amazonaws.com/tcmg476/http_access_log'
    LOCAL_FILE = 'local_copy.log'

    # Use urlretrieve() to fetch a remote copy and save into the local file path
    local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE, lambda x,y,z: print('.', end='', flush=True) if x % 100 == 0 else False)

#moves the log into a searchable list
FILE_NAME = 'local_copy.log'

with open(FILE_NAME) as f:
    requests = [line.rstrip('\n') for line in f]

#Creates a dictionary of monthnames relating to the datetime number given to them
monthnames = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
}

#Creates a list for each month
January = []
February = []
March = []
April = []
May = []
June = []
July = []
August = []
September = []
October = []
November = []
December = []

#Creates a nested dictionary that details the year and then the month a request was made in
months = {
        1994: {
            "October": 0,
            "November": 0,
            "December": 0
        },
        1995: {
            "January": 0,
            "February": 0,
            "March": 0,
            "April": 0,
            "May": 0,
            "June": 0,
            "July": 0,
            "August": 0,
            "September": 0,
            "October": 0
        }
}

#Creates a dictionary where numbers relate to weekdays for later use with days dictionary
weekdays = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
}

#Creates blank dictionary to put the number of requests per weekday in
days = {}

#Creates a dictionary to count the number of requests per week in both years of the log
weekbyweek = {}

#Creates a dictionary for the instaces of the 3xx and 4xx status codes
statcodes = {
        "4XX": 0,
        "3XX": 0
}

#Creates a blank dictionary to put the number of requests per file in
files = {}

#Creates an int to count the amount of requests in six months in
sixmonth = 0

#creates a datetime for 11/Oct/1995 and 11/Apr/1995 to compare to requests to return requests in the past six months
lastday = datetime(1995, 10, 11)
firstday = datetime(1995, 4, 11)

#Regex pattern to use
regex = re.compile('(.*?) - - \[(.*?):(.*) .*\] \"[A-Z]{3,6} (.*?) HTTP.*\" (\d{3}) (.+)')

print("\nNow analyzing the log file, this may take a few minutes. Please be patient")
for line in requests:
    parts = regex.split(line)
    
    #Continues to the next line if the line does not have enough values
    if len(parts) < 8:
        requests.remove(line)
        continue
    
    #Pulls the date of the request out of the parts list
    reqdate = datetime.strptime(parts[2], '%d/%b/%Y')

    #If the date of the request is in the 6 month period increments the counter
    if reqdate <= lastday and reqdate >= firstday:
        sixmonth += 1

    #Checks if day is in day dictionary, increments counter if it is already there, adds the day to the dictionary if it is not
    day = weekdays[reqdate.weekday()]
    if day in days:
        days[day] += 1
    else:
        days[day] = 1

    #Number of requests week by week
    week = int(reqdate.strftime("%W"))
    year = reqdate.year
    if year in weekbyweek:
        if week in weekbyweek[year]:
            weekbyweek[year][week] += 1
        else:
            weekbyweek[year][week] = 1
    else:
        weekbyweek[year] = {week: 1}

    #Increment month counter
    month = reqdate.month
    months[year][monthnames[month]] += 1

    #Appends line to list for each month
    if monthnames[month] == 'January':
        January.append(line)
    elif monthnames[month] == 'February':
        February.append(line)
    elif monthnames[month] == 'March':
        March.append(line)
    elif monthnames[month] == 'April':
        April.append(line)
    elif monthnames[month] == 'May':
        May.append(line)
    elif monthnames[month] == 'June':
        June.append(line)
    elif monthnames[month] == 'July':
        July.append(line)
    elif monthnames[month] == 'August':
        August.append(line)
    elif monthnames[month] == 'September':
        September.append(line)
    elif monthnames[month] == 'October':
        October.append(line)
    elif monthnames[month] == 'November':
        November.append(line)
    elif monthnames[month] == 'December':
        December.append(line)

    #Checks the status code and determines if it is a 3xx or 4xx error code
    statcode = parts[5]
    family = int(statcode[0])
    if family == 4:
        statcodes["4XX"] += 1
    elif family == 3:
        statcodes["3XX"] += 1

    #Checks the file requested by the request
    filename = parts[4]
    #If file is not already a part of the files directory adds it, adds one to the count if it is already in the directory
    if filename in files:
        files[filename] += 1
    else:
        files[filename] = 1

#returns the number of lines in lines;
#it is also the nubmer of requests in the life of the log
totalreq = len(requests)

#Calculate the percentage of 3xx and 4xx statcodes
perc4xx = round((statcodes["4XX"]/totalreq)*100, 2)
perc3xx = round((statcodes["3XX"]/totalreq)*100, 2)

#Finds the most and least requested files
mostreq = max(files, key=files.get)
leastreq = min(files, key=files.get)

#Prints out the information for the marketing request
print("\nANALYSIS")
print("Number of requests to the server in the last 6 months: " + str(sixmonth))
print("Number of requests in the life of the log: " + str(totalreq))
print("Number of requests each day:")
for day in days.items():
    print(day)
print("\nNumber of requests made week-by-week basis, the week nubmer is what week in the year it is with each week starting on Monday. All days in a new year BEFORE the first Monday of the year are in week zero.")
for year, week in weekbyweek.items():
    print(year, ": ")
    print(week)
print("\nNumber of requests per month, further broken down by what year they were made in:")
for year, month in months.items():
    print(year, ": ")
    for num, count in month.items():
        print(num, ": ", count)
print("\nPercentage of requests that were not successful: " + str(perc4xx) + "%")
print("Percentage of requests that were redirected elsewhere: " + str(perc3xx) + "%")
print("The most requested file is: " + str(mostreq))
print("The least requested file is: " + str(leastreq))

print("Now creating smaller files for each month of the log")
jan = open('jan.txt', 'w')
for line in January:
    jan.write(f"{line}\n")
feb = open('feb.txt', 'w')
for line in February:
    feb.write(f"{line}\n")
mar = open('mar.txt', 'w')
for line in March:
    mar.write(f"{line}\n")
apr= open('apr.txt', 'w')
for line in April:
    apr.write(f"{line}\n")
may = open('may.txt', 'w')
for line in May:
    may.write(f"{line}\n")
jun = open('jun.txt', 'w')
for line in June:
    jun.write(f"{line}\n")
jul = open('jul.txt', 'w')
for line in July:
    jul.write(f"{line}\n")
aug = open('aug.txt', 'w')
for line in August:
    aug.write(f"{line}\n")
sep = open('sep.txt', 'w')
for line in September:
    sep.write(f"{line}\n")
octo = open('oct.txt', 'w')
for line in October:
    octo.write(f"{line}\n")
nov = open('nov.txt', 'w')
for line in November:
    nov.write(f"{line}\n")
dec = open('dec.txt', 'w')
for line in December:
    dec.write(f"{line}\n")
print("Program complete")
