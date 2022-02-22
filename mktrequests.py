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

#Creates a dictionary of months and instances in each month
months = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0
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

    #Increment month counter
    months[reqdate.month] += 1

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

#returns the number of lines in requests;
#it is also the nubmer of requests in the life of the log
totalreq = len(requests)

#Calculate the percentage of 3xx and 4xx statcodes
perc4xx = round((statcodes["4XX"]/totalreq)*100, 2)
perc3xx = round((statcodes["3XX"]/totalreq)*100, 2)

#Finds the most and least requested files
mostreq = max(files, key=files.get)
leastreq = min(files, key=files.get)

#Prints out the information for the marketing request
print("Part 1")
print("Here are the number of requests to the server in the last 6 months: " + str(sixmonth))
print("Here are the number of requests in the life of the log: " + str(totalreq))
print("\nPart 2")
print("Here are the number of requests each day:\n" + str(days))
print("Here are the number of requests per month:\n" + str(months))
print("Here are the percentage of requests that were not successful: " + str(perc4xx))
print("Here are the percentage of requests that were redirected elsewhere: " + str(perc3xx))
print("The most requested file is: " + str(mostreq))
print("The least requested file is: " + str(leastreq))
