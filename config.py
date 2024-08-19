######### CONFIG #########

configVersion = 1

URL = "/documents/get.aspx?type=menuplan&menueplanid=364606&startdate="+startdate.strftime("%d%m%Y")+"&enddate="+enddate.strftime("%d%m%Y")+"&price=hide&ext=xls&title=Speiseplan-Geschwister-Scholl&isFixedPricePlan=false&showProductId=false&showAppro=true&showAllergAbbr=false&showAllergAbbrPerComp=false&nutrients=hide&menulines=513112,513113&timerange=week&format=A4&printlanguagecode=German&languagecode=D&showThumbs=0", headers={"Host": "speiseplanung.apetito.de", "Accept": "*/*", "Accept-Language": "de,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Referer": " https://speiseplanung.apetito.de/documents/get.aspx?type=printannouncement&startDate=18122023&endDate=22122023&menuePlanId=364606&menulines=513112,513113&printlanguagecode=German&multiLingual=true&token=D826DD11269A4473369AF4C8FA652B09&languagecode=D"

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
                      
# The time formats used. For Documentation, please visit: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
dayFormat = "%d" # Format for the day.
monthFormat = "%B" # Format for the month.
allMonths = False # If True, all months will be filled in. If False, only the first month field and fields where it changes will be filled in. All others contain monthEmpty.
monthEmpty = "&nbsp;&nbsp;&nbsp;"
wdFormat = "%a" # Format for the weekday.
tsTimeFormat = "Aktualisiert am %d.%m. um %X." # Format for the timestamp in the plan.


locale.setlocale(locale.LC_ALL, 'de_DE') # Language setting

template = open("Template.txt", "r").read() # The Template used for the plan.
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
