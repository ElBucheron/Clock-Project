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

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False,
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

PROBA = [16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16]
CLEARED = True

TABLEAU_LEDS = []
TABLEAU_SNOW = []
TABLEAU_HORLOGE = []
TABLEAU_SNOW = []
showing = 'TABLEAU_HORLOGE'

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

def horloge():
    global default
    global TABLEAU_HORLOGE

    "Affichage de l'heure"
    tz = pendulum.timezone('Europe/Paris')
    heure = dt.datetime.now(tz).hour
    minutes = dt.datetime.now(tz).minute
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
                #TABLEAU_SNOW[i][j] = afficheCiffre[x][y]
                y = y + 1
            x = x + 1
            y = 0
        if (k == 1):
            coord += 4
            #TABLEAU_HORLOGE[coord][1] = default[1]
            #TABLEAU_HORLOGE[coord][2] = default[1]
            #TABLEAU_HORLOGE[coord][4] = default[1]
            #TABLEAU_HORLOGE[coord][5] = default[1]
            coord += 1
            #TABLEAU_HORLOGE[coord][1] = default[1]
            #TABLEAU_HORLOGE[coord][2] = default[1]
            #TABLEAU_HORLOGE[coord][4] = default[1]
            #TABLEAU_HORLOGE[coord][5] = default[1]
            
            #TABLEAU_SNOW[coord][2] = 2
            #TABLEAU_SNOW[coord][4] = 2
            coord += 2
        else:
            coord += 4
    

def blinking():
    global showing

    if(showing == 'TABLEAU_HORLOGE'):
        showing = 'TABLEAU_SNOW'
    else:
        showing = 'TABLEAU_HORLOGE'
    tableauVersLEDS()


def tableauVersLEDS():
    global COULEURS
    global TABLEAU_LEDS

    #if(showing == 'TABLEAU_HORLOGE'):
    tab = TABLEAU_LEDS
    #else:
        #tab = TABLEAU_SNOW

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


def removeSnowLine():
    global TABLEAU_SNOW
    global PROBA
    
    for i in range(32):
        for j in reversed(range(1,8)):
            TABLEAU_SNOW[i][j] = TABLEAU_SNOW[i][j-1]
        TABLEAU_SNOW[i][0] = default[0]
    for idx, val in enumerate(PROBA):
        if val < 10:
            PROBA[idx] += 2
    


def snow():
    global TABLEAU_HORLOGE
    global TABLEAU_SNOW
    global TABLEAU_LEDS
    global PROBA
    global CLEARED

    initTableauLeds()

    removeLine = 0
    for i in range(32):
        if(TABLEAU_SNOW[i][7] != default[0]):
            removeLine += 1
        for j in reversed(range(1,8)):
            #if(TABLEAU_SNOW[i][j] == 0):
            if(TABLEAU_SNOW[i][j-1] != default[0] and TABLEAU_SNOW[i][j] == default[0]):
                TABLEAU_SNOW[i][j] = TABLEAU_SNOW[i][j-1]
                TABLEAU_SNOW[i][j-1] = default[0]
    
    if removeLine == 0:
        CLEARED = True

    #removeSnowLine()

    num = randrange(32)
    if(randrange(100) < PROBA[num]):
        TABLEAU_SNOW[num][0] = "#00C9FF"
        PROBA[num] -= 2
    
    for i in range(32):
        for j in range(8):
            if(TABLEAU_HORLOGE[i][j] == default[0]):
                TABLEAU_LEDS[i][j] = TABLEAU_SNOW[i][j]
            else:
                TABLEAU_LEDS[i][j] = TABLEAU_HORLOGE[i][j]


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


def initTableauSnow():
    global TABLEAU_SNOW
    global default
    
    TABLEAU_SNOW = []
    for i in range(32):
    	TABLEAU_SNOW.append([default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]])
    
    
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


def terminateProcess(signalNumber, frame):
    pixels.fill((0, 0, 0))
    pixels.show()
    exit(0)


if(__name__ == '__main__'):

    signal.signal(signal.SIGTERM, terminateProcess)

    try:
        print("[!] Press ctrl-c to exit")

        print("Reinitialisation des tableaux...")
        initTableauHorloge()
        initTableauSnow()
        initTableauLeds()
        horloge()

        changeHeure = 0
        while True:
            minutes = dt.datetime.now().minute
            minutesNow = minutes % 10

            if(minutesNow != changeHeure):
                #initBackground()
                horloge()
                changeHeure = minutesNow

                if minutesNow == 0:
                    CLEARED = False
            
            if CLEARED == False:
                removeSnowLine()


            snow()
            tableauVersLEDS()
            #blinking()
            #time.sleep(uniform(0.1, 0.4))
            time.sleep(0.4)

    except KeyboardInterrupt:
        terminateProcess(0,0)
