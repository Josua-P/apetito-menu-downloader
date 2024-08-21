configVersion = 1 #DO NOT CHANGE!

URL = ""

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


language = 'de_DE' # Language setting compliant to POSIX Standard (e.g. "en_US" -> English)

template = open("Template.txt", "r").read() # The Template used for the plan.

      # DEBUG ZONE #

debugMode = False # Prints debug information
      
saveSheet = False # Saves the sheet to a file for debugging purposes.

cooldown = 20 # How many seconds to wait between connection attempts

attempts = 10 # After this many failed connections, the program will stop connecting and resume schedule. The plan is not updated.

timeout = None # Connection Timeout
