# apetito-menu-downloader
Simple Python program that can download menu plans from Apetito

[German Readme](https://github.com/Josua-P/apetito-menu-downloader/blob/main/README.de-DE.md)

## How to use
This Program downloads a menu from the food deliverer Apetito and puts the data into a pre-defined Template. It is optimized on HTML, so you can display the data on e.g. a screen for all coworkers / students to see. It can be used to compile a printed sheet as well.

## How to set up
**Please note:** If you understand these instructions, you can use any browser that supports them. <br> They have been written for firefox, so if you don't understand them, *please use firefox!*
1. Download and unpack the starterpack.zip file from the latest release.
1. In a browser, go to the plan you want to display and hit export.
2. There, select "print notice" and make the appropiate settings.
3. After doing this, you should find a button titled "Export Excel". *Before* you press it, press right click and activate inspecting mode (press Q). There, go to the network analysis tool. When you have found it, hit the button.
4. The file you get now is irrelevant, you don't need to save it. The relevant part is that now, the packet for the download should be displayed in the dev console, top entry. Click it.
5. On the right, a little window should open, showing information about the packet. Copy the url in it's entirety and paste it into the config file (config.py) at the URL entry (probably at the top). ***The braces have to stay!***
6. Now (in the config), search the url for the entries startdate und entdate. They should look something like this:
   ```
   ...&startdate=123456&enddate=987654&...
   ```
8. Replace the two 6-digit numbers with two curly brackets ( ```{}``` ). This enables the program to dynamically change the plan's timeframe. It should look something like this:
   ```
   ...&startdate={}&enddate={}&...
   ```
10. Finally, in the packet window, search the request headers (the lower ones) for the values authentication and cookie.
11. Paste these strings into the authentication file (auths.txt). The first line is the authentication, the second line the cookie.
    
   ***Be careful!*** These strings can be used to do *anything* on your account, including transactions and orders. You should *never* give them to anyone, even when asked. If they are leaked, immediately go to your Apetito account settings and sign out on all devices. This will require a complete redo of steps 2-5 and 9-10.


### The config
The config delivered with the starterpack works for most cases. One thing you might be interested in is changing the program's language to display months and weekdays correctly. Just change the language tag to your [POSIX language code](https://learn.microsoft.com/en-us/globalization/locale/other-locale-names#posix). The config itself is also commented, so you'll mostly see there what each option does.

If you want to add your own touch to the program, it might be worth knowning that the entire config.py-file is executed on startup. This means that, if you want to add a function, variables etc, you should add them there, so you can better update the program if a new release comes out, as the config is meant to be persistent over updates.

### The template
The program uses the file "Template.html" (per default) to compile its data into a usable file. This works by it replacing certain tags in the file with data:
 - ```{a[day]}``` and ```{b[day]}``` placehold for the menu lines, where day means days from the startdate (e.g. 0 for the startdate)
- ```{d[day]}``` gives the day.
- ```{m[day]}``` gives the month or the content of monthEmpty (see above).
- ```{wd[day]}``` gives the weekday.
- ```{ts}``` gives the timestamp of the plan. The format can be specified with tsTimeFormat.
- ```{kw}``` gives the calendar week.

The starterpack also contains an example template, so you can get a feeling for the syntax.

If any other placeholders are required, feel free to insert them in line 91.

## Problems?

If any problems or bugs should arise, please feel free to [open an issue](https://github.com/Josua-P/apetito-menu-downloader/issues). I will try to help you as soon as I can!
