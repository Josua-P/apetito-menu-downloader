######### IMPORT #########

import datetime
import time
import http.client
import locale
import zipfile

######## FUNCTIONS #######

class FileLikeBytes():
    def __init__(self, content=b''):
        self.content=content
        self.cursor=0

    def write(self, content):
        #self.content=self.content[:cursor]+content+self.content[cursor:]
        self.content+=content

    def read(self, amount=-1):
        old_cursor=self.cursor
        if amount==-1 or amount>=len(self.content)-self.cursor:
            self.cursor=len(self.content)
        else:
            self.cursor+=amount
        return self.content[old_cursor:self.cursor]

    def seekable(self):
        return True

    def seek(self, n, mode=0):
        if mode==0:
            newcursor=n
        elif mode==1:
            newcursor=self.cursor+n
        elif mode==2:
            newcursor=len(self.content)+n
        else:
            raise ValueError
        if newcursor<0:
            self.cursor=0
        elif newcursor>len(self.content):
            self.cursor=len(self.content)
        else:
            self.cursor=newcursor
        return self.cursor

    def tell(self):
        return self.cursor

def readZipFile(byt):
    file=FileLikeBytes(byt)
    zipF=zipfile.ZipFile(file)
    return zipF.open("web.csv").read().decode("utf-8")

def extractInfo(csv):
    lines=csv.split("\n")
    return list(map(lambda x : x.split(";")[:4], lines[1:]))

def readplan(byt):
    ret={}
    for i in extractInfo(readZipFile(byt)):
        try:
            date=datetime.datetime.strptime(i[0], "%d.%m.%Y").date()
            if not date in ret:
                ret[date]={}
            ret[date][i[2]]=i[3]
        except:
            pass
    return ret

def formatMenuEntry(text):
    lines = text.split(", ")
    for i in noDisplay:
        try:
            lines.remove(i)
        except:
            pass
    ret=""
    for i in lines:
        ret+="- "+i+"<br>"
    return ret

def dateToOffset(date):
    return (date-initDate).days

########## CODE ##########
config = open("config.py", "r").read()
configVersion = -1
exec(config)
if configVersion != 1:
    raise(Exception("Wrong config version!"))

auths = open("auths.txt", "r").readlines()
authorization = auths[0].strip()
#cookie = auths[1].strip()

locale.setlocale(locale.LC_ALL, language)

cAttempts=0
while True:
    conn=http.client.HTTPSConnection("mealmaster.apetito.de", timeout=timeout) #Connection to the server
    connected=True
    while connected:
        if conn:
            
            t=datetime.date.today()
            if useWholeWeeks:
                startdate=t-datetime.timedelta(days=t.weekday())
            else:
                startdate=t
            enddate=startdate+datetime.timedelta(days=7)

            req = "/api/printing-configurations/"+ID+"/file?fileType=csv&language="+language+"&startOffset="+str(dateToOffset(startdate))+"&endOffset="+str(dateToOffset(enddate)) #URL.format(startdate.strftime("%d%m%Y"), enddate.strftime("%d%m%Y")).replace(" ", "%20")
            if debugMode:
                print("Requesting to "+req)
            
            conn.request("GET", req, headers={"Host": "mealmaster.apetito.de", "Accept": "*/*", "Accept-Language": "de,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Authorization": authorization, "DNT": " 1", "Connection": " keep-alive", "Sec-Fetch-Dest": " empty", "Sec-Fetch-Mode": " cors", "Sec-Fetch-Site": " same-origin"})
            resp=conn.getresponse()
            timestamp = datetime.datetime.now()
            respb=resp.read() #the servers response data in bytes
            if len(respb)>0:
                cAttempts=0
                if saveSheet:
                    try:
                        open("latest.zip", "wb").write(respb)
                    except PermissionError:
                        print("Sheet unsaved: Access denied")
                plan = readplan(respb)
                A=[]
                B=[]
                T=[] # Days as datetime.date

                for i in range(7):
                    day = startdate+datetime.timedelta(days=i)
                    if day in plan:
                        menues=plan[day]
                        if "Menü 1" in menues:
                            A.append(formatMenuEntry(menues["Menü 1"]))
                        else:
                            A.append("")
                        if "Menü 2" in menues:
                            B.append(formatMenuEntry(menues["Menü 2"]))
                        else:
                            B.append("")
                        T.append(day)
                    elif not (day.weekday() in disabledWeekdays):
                        A.append("")
                        B.append("")
                        T.append(day)
                        
                D=[]  # Days
                M=[]  # Months
                WD=[] # Weekdays
                for t in T: # disassembling T into D, ST, WD and M
                    D.append(t.strftime(dayFormat))
                    WD.append(t.strftime(wdFormat))
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
                
                result = template.format(a=A, b=B, d=D, m=M, wd=WD, kw=startdate.strftime("%W"), ts=timestamp.strftime(tsTimeFormat), auf="{", zu="}") # This inserts the values into the template
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
                connected=False
                cAttempts+=1
        else:
            connected=False
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
