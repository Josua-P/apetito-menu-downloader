######### IMPORT #########

import datetime
import time
import http.client
import xlrd
from xlrd.book import *
from xlrd.sheet import *
import locale

########## CODE ##########
config = open("config.py").read()
configVersion = -1
exec(config)
if configVersion != 1:
    raise("Wrong config version!")

auths = open("auths.txt", "r").readlines()
authorization = auths[0].strip()
cookie = auths[1].strip()

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
            
            conn.request("GET", URL, "Authorization": authorization, "DNT": " 1", "Connection": " keep-alive", "Cookie": cookie, "Sec-Fetch-Dest": " empty", "Sec-Fetch-Mode": " cors", "Sec-Fetch-Site": " same-origin"})
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
