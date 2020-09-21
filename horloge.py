# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import datetime as dt
import pendulum
import math
import signal
from random import randrange
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

TABLEAU = []
TABLEAUBIS = []
showing = 'TABLEAU'

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

def horloge():
    global default
    global TABLEAU

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

    coord = 14
    for k in range(4):
        afficheCiffre = CHIFFRE[afficheHeure[k]]
        x = 0
        y = 0
        for i in range(coord, coord+3):
            for j in range(1, 6):
                TABLEAU[i][j] = afficheCiffre[x][y]
                TABLEAUBIS[i][j] = afficheCiffre[x][y]
                y = y + 1
            x = x + 1
            y = 0
        if (k == 1):
            coord = coord + 4
            TABLEAU[coord][2] = default[1]
            TABLEAU[coord][4] = default[1]
            #TABLEAUBIS[coord][2] = 2
            #TABLEAUBIS[coord][4] = 2
            coord = coord + 2
        else:
            coord = coord + 4
    
    tableauVersLEDS()


def blinking():
    global showing

    if(showing == 'TABLEAU'):
        showing = 'TABLEAUBIS'
    else:
        showing = 'TABLEAU'
    tableauVersLEDS()


def tableauVersLEDS():
    global COULEURS

    #if(showing == 'TABLEAU'):
    tab = TABLEAU
    #else:
        #tab = TABLEAUBIS

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


def snow():
    global TABLEAU
    global TABLEAUBIS

    initTableau()
    horloge()
    
    removeLine = 0
    for i in range(32):
        if(TABLEAUBIS[i][7] == 0):
            removeLine = removeLine + 1
        for j in reversed(range(1,8)):
            #if(TABLEAUBIS[i][j] == 0):
            if(TABLEAUBIS[i][j-1] != 0):
                TABLEAUBIS[i][j] = TABLEAUBIS[i][j-1]
                TABLEAUBIS[i][j-1] = 0
    
    if(removeLine <= 0):
        for i in range(32):
            for j in reversed(range(1,8)):
                TABLEAUBIS[i][j] = TABLEAUBIS[i][j-1]
            TABLEAUBIS[i][0] = 0
    
    
    if(randrange(100) < 5):
        num = randrange(32)
        TABLEAUBIS[num][0] = 6
    
    for i in range(32):
        for j in range(8):
            if(TABLEAU[i][j] == 0):
                TABLEAU[i][j] = TABLEAUBIS[i][j]



    tableauVersLEDS()


def initTableau():
    global TABLEAU
    global default
   
    TABLEAU = []
    for i in range(32):
    	TABLEAU.append([default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]])

    #TABLEAU = [[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]]]
    

def initTableaubis():
    global TABLEAUBIS
    global default
    
    TABLEAUBIS = []
    for i in range(32):
    	TABLEAUBIS.append([default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]])
    
    #TABLEAUBIS = [[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]],[default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]]]

    
def initBackground():
    print("Choosing background...")
    #num = str(randrange(1,5))
    
    f = open("/root/Clock-Project/Backgrounds/" + "1" + ".txt", "r")

    idx = 0
    for line in f:
        #Removing \n
        line = line[:-1]
        pixel = line.split("|")
        pixel.reverse();
        for idx2 in reversed(range(len(TABLEAU))):
            TABLEAU[idx2][idx] = str(pixel[idx2])
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
        initTableau()
        initTableaubis()
        horloge()
        initBackground()

        changeHeure = 0
        while True:
            minutes = dt.datetime.now().minute
            minutesNow = minutes % 10

            if(minutesNow != changeHeure):
                horloge()
                #if(minutesNow == 0):
                    #initTableaubis()
                changeHeure = minutesNow

            #snow()
            blinking()
            tableauVersLEDS()
            time.sleep(1)

    except KeyboardInterrupt:
        terminateProcess(0,0)
