# Home-Monitoring-Python-Two
Part 2 of developing a home monitoring system.

PIR example on a Raspberry Pi.

You need: Raspberry Pi, PIR Sensor, LED

The program senses movements through a PIR sensor. A movement object is created with the count and datetime passed in, 
this is stored in a list. The list is saved to a file periodically. 
The program will also flash an LED to show it has detected movement.
This program now connects over the internet to AdafruitIO to be able to display data.
Currently it only sends basic data to show that movement has occured.

Part 1 here: https://github.com/aldersjus/Home-Monitoring-System
