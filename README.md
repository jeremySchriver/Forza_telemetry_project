Project to capture and record telemtry data from Forza Motorsport 8 using their UDP data out feature set

Forza UDP packet information:
    -https://support.forzamotorsport.net/hc/en-us/articles/21742934024211-Forza-Motorsport-Data-Out-Documentation

Forza Car Ordinal Information:
    -https://forums.forza.net/t/car-ordinal-list-for-forza-motorsport/649188/2

Accredited Sources Used:
    -https://github.com/austinbaccus/forza-telemetry
    -https://github.com/makvoid/Blog-Articles/blob/main/Forza-Telemetry/util/led.py

This is currently a work in progress and is not intended to be run as an application. Modules will be outlined as they are created and tested.

Setup
    -Refer to the requirements.txt file for all required python libraries that need installed
    -Download a copy of the master branch of the repo and place in a local folder to be run in an IDE of your choice.

Telemetry Capture Data To CSV:
    -Run telemetryCapture.py in terminal

Adding car information to the database:
    -Run carDBAdd.py in terminal

Normalize and graph captured data:
    -Run csvFiller.py in terminal and follow prompts with yes/no answers