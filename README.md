# apetito-menu-downloader
Simple Python program that can download menu plans from Apetito

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
   ```...&startdate=123456&enddate=987654&...```
8. Replace the two 6-digit numbers with two curly brackets ( ˋ{}ˋ ). This enables the program to dynamically change the plan's timeframe. It should look something like this:
   ```...&startdate={}&enddate={}&...```
9. Finally, in the packet window, search the request headers (the lower ones) for the values authentication and cookie.
10. Paste these strings into the authentication file (auths.txt). The first line is the authentication, the second line the cookie.
   ***Be careful!*** These strings can be used to do *anything* on your account, including transactions and orders. You should *never* give them to anyone, even when asked. If they are leaked, immediately go to your Apetito account settings and sign out on all devices. This will require a complete redo of steps 2-5 and 9-10.
