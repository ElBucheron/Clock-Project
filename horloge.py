# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import datetime as dt
import pendulum
import math
import signal
from random import randrange
from random import uniform
from cozy_fire import fire

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 256

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=ORDER)

default = ["#000000", "#FA7921"]

ZERO = [[default[1],default[1],default[1],default[1],default[1]],[default[1],default[0],default[0],default[0],default[1]],[default[1],default[1],default[1],default[1],default[1]]]
UN = [[default[0],default[0],default[0],default[0],default[1]],[default[1],default[1],default[1],default[1],default[1]],[default[0],default[1],default[0],default[0],default[1]]]
DEUX = [[default[1],default[1],default[1],default[0],default[1]],[default[1],default[0],default[1],default[0],default[1]],[default[1],default[0],default[1],default[1],default[1]]]
TROIS = [[default[1],default[1],default[1],default[1],default[1]],[default[1],default[0],default[1],default[0],default[1]],[default[1],default[0],default[0],default[0],default[1]]]
QUATRE = [[default[0],default[1],default[1],default[1],default[1]],[default[0],default[0],default[1],default[0],default[0]],[default[1],default[1],default[1],default[0],default[0]]]
CINQ = [[default[1],default[0],default[1],default[1],default[1]],[default[1],default[0],default[1],default[0],default[1]],[default[1],default[1],default[1],default[0],default[1]]]
SIX = [[default[1],default[0],default[1],default[1],default[1]],[default[1],default[0],default[1],default[0],default[1]],[default[1],default[1],default[1],default[1],default[1]]]
SEPT = [[default[1],default[1],default[1],default[1],default[1]],[default[1],default[0],default[0],default[0],default[0]],[default[1],default[0],default[0],default[0],default[0]]]
HUIT = [[default[1],default[1],default[1],default[1],default[1]],[default[1],default[0],default[1],default[0],default[1]],[default[1],default[1],default[1],default[1],default[1]]]
NEUF = [[default[1],default[1],default[1],default[1],default[1]],[default[1],default[0],default[1],default[0],default[1]],[default[1],default[1],default[1],default[0],default[1]]]
CHIFFRE = [ZERO,UN,DEUX,TROIS,QUATRE,CINQ,SIX,SEPT,HUIT,NEUF]

TABLEAU_LEDS = []
TABLEAU_HORLOGE = []
MODE_BRIGHT = 'DAY'

def hex_to_rgb(value):
    global MODE_BRIGHT

    value = value.lstrip('#')
    lv = len(value)

    if MODE_BRIGHT == 'DAY':
        rgb_values = tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))
    elif MODE_BRIGHT == 'EVENING':
        rgb_values = tuple(int(int(value[i:i+lv//3], 16)/2) for i in range(0, lv, lv//3))
    elif MODE_BRIGHT == 'NIGHT':
        rgb_values = tuple(int(int(value[i:i+lv//3], 16)/10) for i in range(0, lv, lv//3))
    elif MODE_BRIGHT == 'OFF':
        turnOffLeds()

    return rgb_values

def horloge(heure, minutes):
    global default
    global TABLEAU_HORLOGE

    "Affichage de l'heure"
    if(heure > 9):
        heure1 = heure // 10 ** int(math.log(heure, 10))
        heure2 = heure % 10
    else:
        heure1 = 0
        heure2 = heure
    if(minutes > 9):
        minute1 = minutes // 10 ** int(math.log(minutes, 10))
        minute2 = minutes % 10
    else:
        minute1 = 0
        minute2 = minutes

    afficheHeure = [minute2, minute1, heure2, heure1]
    #print("Heure:", afficheHeure)

    coord = 7
    for k in range(4):
        afficheCiffre = CHIFFRE[afficheHeure[k]]
        x = 0
        y = 0
        for i in range(coord, coord+3):
            for j in range(1, 6):
                TABLEAU_HORLOGE[i][j] = afficheCiffre[x][y]
                y = y + 1
            x = x + 1
            y = 0
        if (k == 1):
            coord += 4
            coord += 1
            
            coord += 2
        else:
            coord += 4
    

def tableauVersLEDS():
    global COULEURS
    #global TABLEAU_LEDS
    global TABLEAU_HORLOGE

    tab = TABLEAU_HORLOGE

    i = 0
    led = 0
    while i < 31:
        for j in reversed(range(8)):
            pixels[led] = hex_to_rgb(tab[i][j])
            led = led + 1
        i = i + 1

        for j in range(8):
            pixels[led] = hex_to_rgb(tab[i][j])
            led = led + 1
        i = i + 1

    pixels.show()


def initTableauLeds():
    global TABLEAU_LEDS
    global default
   
    TABLEAU_LEDS = []
    for i in range(32):
    	TABLEAU_LEDS.append([default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]])


def initTableauHorloge():
    global TABLEAU_HORLOGE
    global default
   
    TABLEAU_HORLOGE = []
    for i in range(32):
    	TABLEAU_HORLOGE.append([default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]])

    
def initBackground():
    print("Choosing background...")
    num = str(randrange(1,3))
    
    f = open("/root/Clock-Project/Backgrounds/" + num + ".txt", "r")

    idx = 0
    for line in f:
        #Removing \n
        line = line[:-1]
        pixel = line.split("|")
        pixel.reverse();
        for idx2 in reversed(range(len(TABLEAU_HORLOGE))):
            TABLEAU_HORLOGE[idx2][idx] = str(pixel[idx2])
        idx += 1
    f.close()

def turnOffLeds():
    pixels.fill((0, 0, 0))
    pixels.show()

def terminateProcess(signalNumber, frame):
    turnOffLeds()
    exit(0)


if(__name__ == '__main__'):

    signal.signal(signal.SIGTERM, terminateProcess)

    try:
        print("[!] Press ctrl-c to exit")

        print("Reinitialisation des tableaux...")
        initTableauHorloge()
        initTableauLeds()
        
        tz = pendulum.timezone('Europe/Paris')
        
        #heure = dt.datetime.now(tz).hour
        #minutes = dt.datetime.now(tz).minute
        
        #horloge(heure, minutes)
        #tableauVersLEDS()

        changeHeure = int
        changeMinute = int
        while True:

            heure = dt.datetime.now(tz).hour
            minutes = dt.datetime.now(tz).minute
    
            minutesNow = minutes % 10

            if(heure != changeHeure):
                #initBackground()
                if(MODE_BRIGHT == 'DAY'):
                    if(heure >= 18 and heure < 21):
                        MODE_BRIGHT = 'EVENING'

                elif(MODE_BRIGHT == 'EVENING'):
                    if(heure >= 21):
                        MODE_BRIGHT = 'NIGHT'
                
                elif(MODE_BRIGHT == 'NIGHT'):
                    if(heure >= 0 and heure < 8):
                        MODE_BRIGHT = 'OFF'

                elif(MODE_BRIGHT == 'OFF'):
                        if(heure >= 8 and heure < 19):
                            MODE_BRIGHT = 'DAY'

                changeHeure = heure

            if(minutesNow != changeMinute and MODE_BRIGHT != 'OFF'):
                horloge(heure, minutes)
                tableauVersLEDS()
                changeMinute = minutesNow

            #tableauVersLEDS()
            #time.sleep(uniform(0.1, 0.4))
            time.sleep(1)

    except KeyboardInterrupt:
        terminateProcess(0,0)
