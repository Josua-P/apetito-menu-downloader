# apetito-menu-downloader
Simple Python program that can download menu plans from Apetito

[German Readme](https://github.com/Josua-P/apetito-menu-downloader/blob/main/README.de-de.md)

## How to use
This Program downloads a menu from the food deliverer Apetito and puts the data into a pre-defined Template. It is optimized on HTML, so you can display the data on e.g. a screen for all coworkers / students to see. It can be used to compile a printed sheet as well.

## How to set up
**Please note:** If you understand these instructions, you can use any browser that supports them. <br> They have been written for firefox, so if you don't understand them, *please use firefox!*
1. Download and unpack the starterpack.zip file from the latest release.
1. In a browser, go to the plan you want to display and press "Print".
2. There, select "Menu" and the document type "CSV". Remember the start date, it is required later.
3. After doing this, you should find a button titled "Create". *Before* you press it, press right click and activate inspecting mode (Q). There, go to the network analysis tool. When you have found it, press the button.
4. The file you get now is irrelevant, you don't need to save it. The relevant part is that now, the packet for the download should be displayed in the dev console. There will be two packets, one is of the type "GET". Click that one.
5. On the right, a little window should open, showing information about the packet. Copy the ID after "mealmaster.apetito.de/api/printing-configurations" up to the next slash and paste it into the config file (config.py) at the ID entry (probably at the top). ***The braces have to stay!***
After this, the line should look something like this:<br><br>
   ```
   ID = "12345678-abcd-cdef-1357-2468acef4321"
   ```
6. Now  search the url for the entry startOffset. It should be followed by a number.
7. Now it's time to calculate: Subtract the number off the selected start date.<br>e.g.: If the start date was 26th July 2026, and an offset of 15, your result would be 11th July 2026.
8. That date must now be entered into the config:<br><br>
   ```
   initDate = datetime.date(<year>, <month>, <day>)
   ```
   For example, the 11th July 2026 would be noted as:<br><br>
   ```
   datetime.date(2026, 7, 11)
   ```
10. Finally, in the packet window, search the request headers (the lower ones) for the value authentication.
11. Paste this string into the authentication file (auths.txt).
    
   ***Be careful!*** That string can be used to do *anything* on your account, including transactions and orders. You should *never* give it to anyone, even when asked. If they are leaked, *immediately* change your password. This will require a complete redo of steps 2-10.


### The config
The config delivered with the starterpack works for most cases. A setting you might be interested in is changing the program's language to display months and weekdays correctly. Just change the language tag to your [POSIX language code](https://learn.microsoft.com/en-us/globalization/locale/other-locale-names#posix). The config itself is also commented, so you'll mostly see there what each option does.

If you want to add your own touch to the program, it might be worth knowning that the entire config.py-file is executed on startup. This means that, if you want to add a function, variables etc, you should add them there, so you can better update the program if a new release comes out, as the config is meant to be persistent over updates.

### The template
The program uses the file "Template.html" (per default) to compile its data into a usable file. This works by it replacing certain tags in the file with data:
 - ```{a[day]}``` and ```{b[day]}``` placehold for the menu lines, where day means days from the startdate (e.g. 0 for the startdate)
- ```{d[day]}``` gives the day.
- ```{m[day]}``` gives the month or the content of monthEmpty (see config).
- ```{wd[day]}``` gives the weekday.
- ```{ts}``` gives the timestamp of the plan. The format can be specified with tsTimeFormat.
- ```{kw}``` gives the calendar week.

The starterpack also contains an example template, so you can get a feeling for the syntax.

If any other placeholders are required, feel free to insert them in line 89.

## Problems?

If any problems or bugs should arise, please feel free to [open an issue](https://github.com/Josua-P/apetito-menu-downloader/issues). I will try to help you as soon as I can!
