######### IMPORT #########

import datetime
import time
import http.client
import xlrd
from xlrd.book import *
from xlrd.sheet import *
import locale


######### CONFIG #########

filepath="output.html" # Where to save the resulting file

downloadHour = 7    # When to download the plan
downloadMinute = 55 
def waittime():     # Determines the waiting time for any given point in time. Feel free to change it if you want to refresh more frequently. Output in seconds.
    t = datetime.datetime.now()
    nextDownload = datetime.datetime(t.year, t.month, t.day+((t.hour>downloadHour+1) or (t.hour==downloadHour and t.minute>downloadMinute-1)), downloadHour, downloadMinute)
    return (nextDownload-t).seconds

disabledWeekdays = [5, 6] # Disable Download on workless Weekdays. Default is [5, 6] for Saturday and Sunday

useWholeWeeks = False # When set to True, the plan displayed will show the calendar week (Monday to Friday).
                      # When set to False, the following 5 Days are displayed (Monday to Friday, Tuesday to Monday, Wednesday to Tuesday, ...)
                      
timeFormat = "%A\n%d.%m." # The time format used. For Documentation, please visit: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
dayFormat = "%d" # Format for the day.
monthFormat = "%B" # Format for the month.
allMonths = False # If True, all months will be filled in. If False, only the first month field and fields where it changes will be filled in. All others contain monthEmpty.
monthEmpty = "&nbsp;&nbsp;&nbsp;"
wdFormat = "%a" # Format for the weekday.
tsTimeFormat = "Aktualisiert am %d.%m. um %X." # Format for the timestamp in the plan.


locale.setlocale(locale.LC_ALL, 'de_DE') # Language setting

template = open("Template vorläufig.txt", "r").read() # The Template used for the plan.
    #
    # It supports the following syntax for replacement:
    #
    # - {a[day]} and {b[day]} placehold for the menu lines, where day means days from the startdate
    #
    # - {t[day]} is used for the date. The format can be specified with timeFormat. (v1.1: Use d, m and wd instead)
    #
    # - {d[day]} gives the day.
    #
    # - {m[day]} gives the month or the content of monthEmpty (see above).
    #
    # - {wd[day]} gives the weekday.
    #
    # - {ts} gives the timestamp of the plan. The format can be specified with tsTimeFormat.
    #
    # - {kw} gives the calendar week.
    #
    # If any other placeholders are required, feel free to insert them in line 146.


      # DEBUG ZONE #

debugMode = True # Prints debug information
      
saveSheet = False # Saves the sheet to a file for debugging purposes.

cooldown = 20 # How many seconds to wait between connection attempts

attempts = 10 # After this many failed connections, the program will stop connecting and resume schedule. The plan is not updated.

timeout = None # Connection Timeout

         # AUTHS #

authorization = ""

cookie = ""

########## CODE ##########
cAttempts=0
while True:
    conn=http.client.HTTPSConnection("speiseplanung.apetito.de", timeout=timeout) #Connection to the server
    connected=True
    while connected:
        if conn:
            
            t=datetime.date.today()
            if useWholeWeeks:
                startdate=t-datetime.timedelta(days=t.weekday())
            else:
                startdate=t
            enddate=startdate+datetime.timedelta(days=7)
            
            conn.request("GET", "/documents/get.aspx?type=menuplan&menueplanid=364606&startdate="+startdate.strftime("%d%m%Y")+"&enddate="+enddate.strftime("%d%m%Y")+"&price=hide&ext=xls&title=Speiseplan-Geschwister-Scholl&isFixedPricePlan=false&showProductId=false&showAppro=true&showAllergAbbr=false&showAllergAbbrPerComp=false&nutrients=hide&menulines=513112,513113&timerange=week&format=A4&printlanguagecode=German&languagecode=D&showThumbs=0", headers={"Host": "speiseplanung.apetito.de", "Accept": "*/*", "Accept-Language": "de,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Referer": " https://speiseplanung.apetito.de/documents/get.aspx?type=printannouncement&startDate=18122023&endDate=22122023&menuePlanId=364606&menulines=513112,513113&printlanguagecode=German&multiLingual=true&token=D826DD11269A4473369AF4C8FA652B09&languagecode=D", "Authorization": authorization, "DNT": " 1", "Connection": " keep-alive", "Cookie": cookie, "Sec-Fetch-Dest": " empty", "Sec-Fetch-Mode": " cors", "Sec-Fetch-Site": " same-origin"})
            resp=conn.getresponse()
            timestamp = datetime.datetime.now()
            respb=resp.read() #the servers response data in bytes
            if len(respb)>0:
                cAttempts=0
                if saveSheet:
                    try:
                        open("latest.xls", "wb").write(respb)
                    except PermissionException:
                        print("Sheet unsaved: Access denied")
                bk = xlrd.open_workbook(file_contents=respb)
                sh = bk.sheet_by_index(0) #the sheet with the plan
                A=[]
                B=[]
                T=[] # Days as datetime.date
                if startdate.weekday()==0: # Code if it's a monday: All Menues are listed consecutively.
                    for i in range(6, 23, 4):
                        A.append(sh.cell_value(rowx=i, colx=1)[0:-2])
                    for i in range(6, 23, 4):
                        B.append(sh.cell_value(rowx=i, colx=2)[0:-2])
                    for i in range(0, 5):
                        T.append((startdate+datetime.timedelta(days=i)))
                else: # Else the programm looks specifically for the gap built in by the website between weeks.
                    row=6
                    for i in range(7):
                        if not (startdate+datetime.timedelta(days=i)).weekday() in [5, 6]:
                            A.append(sh.cell_value(rowx=row, colx=1)[0:-2])
                            B.append(sh.cell_value(rowx=row, colx=2)[0:-2])
                            T.append((startdate+datetime.timedelta(days=i)))
                        row+=4
                        
                D=[]  # Days
                M=[]  # Months
                WD=[] # Weekdays
                ST=[] # Full date as string
                for t in T: # disassembling T into D, ST, WD and M
                    D.append(t.strftime(dayFormat))
                    WD.append(t.strftime(wdFormat))
                    ST.append(t.strftime(timeFormat))
                    if t==T[0] or t.day==1 or allMonths:
                        M.append(t.strftime(monthFormat))
                    else:
                        M.append(monthEmpty)

                if debugMode:
                    print("A=")
                    print(A)
                    print("B=")
                    print(B)
                    print("D=")
                    print(D)
                
                result = template.format(a=A, b=B, t=ST, d=D, m=M, wd=WD, kw=startdate.strftime("%W"), ts=timestamp.strftime(tsTimeFormat), auf="{", zu="}") # This inserts the values into the template
                unsaved=True
                while unsaved:
                    try:
                        with open(filepath, "w") as file:
                            file.write(result)
                        unsaved=False
                    except PermissionException:
                        print("Access to output file denied. Make sure to close all file access after reading!")
                        time.sleep(10)
                        
            else:
                connected=false
                cAttempts+=1
        else:
            connected=false
            cAttempts+=1
            
        # wait until next scheduled download
        if cAttempts>=attempts:
            print("Attempt limit reached. Resuming schedule.")
            cAttempts=0
            wait=waittime()
        elif not connected:
            wait=cooldown
        else:
            wait=waittime()
        time.sleep(wait)
        while datetime.datetime.now().weekday() in disabledWeekdays:
            time.sleep(86400)

#EOF
