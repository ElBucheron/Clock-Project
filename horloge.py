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

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.02, auto_write=False,
                           pixel_order=ORDER)


ZERO = [[2,2,2,2,2],[2,0,0,0,2],[2,2,2,2,2]]
UN = [[0,0,0,0,2],[2,2,2,2,2],[0,2,0,0,2]]
DEUX = [[2,2,2,0,2],[2,0,2,0,2],[2,0,2,2,2]]
TROIS = [[2,2,2,2,2],[2,0,2,0,2],[2,0,0,0,2]]
QUATRE = [[0,2,2,2,2],[0,0,2,0,0],[2,2,2,0,0]]
CINQ = [[2,0,2,2,2],[2,0,2,0,2],[2,2,2,0,2]]
SIX = [[2,0,2,2,2],[2,0,2,0,2],[2,2,2,2,2]]
SEPT = [[2,2,2,2,2],[2,0,0,0,0],[2,0,0,0,0]]
HUIT = [[2,2,2,2,2],[2,0,2,0,2],[2,2,2,2,2]]
NEUF = [[2,2,2,2,2],[2,0,2,0,2],[2,2,2,0,2]]
CHIFFRE = [ZERO,UN,DEUX,TROIS,QUATRE,CINQ,SIX,SEPT,HUIT,NEUF]

TABLEAU = []
TABLEAUBIS = []
showing = 'TABLEAU'

#             noir        blanc          jaune          orange        rouge      violet        bleu       bleu fonce     vert
COULEURS = [(0, 0, 0),(55, 55, 55),(250, 121, 33),(155, 58, 0),(155, 0, 0),(128, 0, 128),(0, 155, 155),(0, 0, 155),(0, 128, 0)]

def horloge():
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

    global TABLEAU

    coord = 14
    for k in range(4):
        afficheCiffre = CHIFFRE[afficheHeure[k]]
        x = 0
        y = 0
        for i in range(coord, coord+3):
            for j in range(1, 6):
                TABLEAU[i][j] = afficheCiffre[x][y]
                #TABLEAUBIS[i][j] = afficheCiffre[x][y]
                y = y + 1
            x = x + 1
            y = 0
        if (k == 1):
            coord = coord + 4
            TABLEAU[coord][2] = 2
            TABLEAU[coord][4] = 2
            #TABLEAUBIS[coord][2] = 2
            #TABLEAUBIS[coord][4] = 2
            coord = coord + 2
        else:
            coord = coord + 4


def blinking():
    global showing

    if(showing == 'TABLEAU'):
        showing = 'TABLEAUBIS'
    else:
        showing = 'TABLEAU'
    tableauVersLEDS()
    pixels.show()


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
            pixels[led] = COULEURS[tab[i][j]]
            led = led + 1
        i = i + 1

        for j in range(8):
            pixels[led] = COULEURS[tab[i][j]]
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

    TABLEAU = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

def initTableaubis():
    global TABLEAUBIS

    TABLEAUBIS = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

    
def initBackground():
    print("Choosing background...")
    num = str(randrange(1,5))
    
    f = open("/root/Clock-Project/Backgrounds/" + num + ".txt", "r")

    for idx, line in enumerate(f):
        if(line[0] == '#'):
            continue
        else:
            #Removing \n
            line = line[:-1]
            #Reversing the string
            line = line[::-1]
            if(idx <= 8):
                for idx2 in range(len(TABLEAU)):
                    TABLEAU[idx2][idx-1] = int(line[idx2])
            else:
                for idx2 in range(len(TABLEAUBIS)):
                    TABLEAUBIS[idx2][(idx-2)%8] = int(line[idx2])

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
        #initBackground()

        changeHeure = 0
        while True:
            #minutes = dt.datetime.now().minute
            #minutesNow = minutes % 10

            #if(minutesNow != changeHeure):
                #if(minutesNow == 0):
                    #initTableaubis()
                #changeHeure = minutesNow

            snow()
            #blinking()
            time.sleep(0.2)

    except KeyboardInterrupt:
        terminateProcess(0,0)
