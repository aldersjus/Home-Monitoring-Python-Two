#Author: Justin Alderson
#This is Part 2 of beginning a home monitoring system.
#Built for Raspberry Pi.
#The program senses movements through a PIR sensor. A movement object
#is created with the count and datetime passed in, this is stored in
#a list. The list is saved to a file periodically. The program will
#also flash an LED to show it has detected movement.

#This program now connects over the internet to AdafruitIO to be able to display data.
#Currently it only sends basic data to show that movement has occured.

#If you try to use this program, I strongly advise you to work through these tutorials. And any linked to it.
####First followed this before changing the code. https://learn.adafruit.com/adafruit-io-basics-digital-input/python-code

####Need to be in this directory to run this code ~/io-client-python/examples/basics
####Need to create a folder to hold this code: /home/pi/Home_Monitor Place all program file in this folder.
####Need a data in this location: /home/pi/Home_Monitor/data.dat

#import RPi.GPIO as GPIO
import time
import datetime
import pickle
import motion
import board
import digitalio

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'secret key goes here'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'username'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'digital' feed
    digital = aio.feeds('digital')
except RequestError: # create a digital feed
    feed = Feed(name="digital")
    digital = aio.create_feed(feed)

#Set up variables
my_GPIO_PIR = digitalio.DigitalInOut(board.D22)
my_GPIO_PIR_previous_value = my_GPIO_PIR.value
my_GPIO_PIR_activated = False
my_GPIO_LED = digitalio.DigitalInOut(board.D11)
my_GPIO_LED.direction = digitalio.Direction.OUTPUT
count = 0
save_count = 0
oclock = 0
movement_detected = []

print("Home movement counter preparing to launch.")

def save():
    data = movement_detected
    save_file = open('/home/pi/Home_Monitor/data.dat','wb')
    pickle.dump(data, save_file)
    save_file.close()


try:
    #Load previously saved data.
    load_file = open('/home/pi/Home_Monitor/data.dat', 'rb')
    data = pickle.load(load_file)
    movement_detected = data
    count = len(movement_detected)
    load_file.close()


except EOFError:
    pass

try:

    time.sleep(2)
    print("Launching.")

    while True:

        #Save periodically.
        if save_count > 500 and oclock.minute == 59:
            save()
            save_count = 0

        #Detect movement.    
        if  my_GPIO_PIR.value == True:
            my_GPIO_PIR_activated = True
            aio.send(digital.key, 1)
            print ("Motion %d " %count)
            print(datetime.datetime.today())
            #Create motion class object here...
            detected = motion.Movement(count,datetime.datetime.today())
            count += 1
            save_count += 1
            #LED on
            my_GPIO_LED.value = True
            #Append to list here
            movement_detected.append(detected)
            time.sleep(1)
        else:
            print('Motion ended')
            my_GPIO_PIR_activated = False
            aio.send(digital.key, 0)
            #LED off
            my_GPIO_LED.value = False


    # avoid timeout from adafruit io
    time.sleep(1)


#Will accept Control C in the terminal to exit program. It will finally print Shutdown message.
except KeyboardInterrupt:

    #SAVE data on close.
    save()
    print("Home Movement Detector Saved Data Shutdown")
