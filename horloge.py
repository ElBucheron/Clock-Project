# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import datetime as dt
import pendulum
import math
import signal
from random import randrange

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


ZERO = [[6,6,6,6,6],[6,0,0,0,6],[6,6,6,6,6]]
UN = [[0,0,0,0,6],[6,6,6,6,6],[0,6,0,0,6]]
DEUX = [[6,6,6,0,6],[6,0,6,0,6],[6,0,6,6,6]]
TROIS = [[6,6,6,6,6],[6,0,6,0,6],[6,0,0,0,6]]
QUATRE = [[0,6,6,6,6],[0,0,6,0,0],[6,6,6,0,0]]
CINQ = [[6,0,6,6,6],[6,0,6,0,6],[6,6,6,0,6]]
SIX = [[6,0,6,6,6],[6,0,6,0,6],[6,6,6,6,6]]
SEPT = [[6,6,6,6,6],[6,0,0,0,0],[6,0,0,0,0]]
HUIT = [[6,6,6,6,6],[6,0,6,0,6],[6,6,6,6,6]]
NEUF = [[6,6,6,6,6],[6,0,6,0,6],[6,6,6,0,6]]
CHIFFRE = [ZERO,UN,DEUX,TROIS,QUATRE,CINQ,SIX,SEPT,HUIT,NEUF]

#TABLEAU = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,7,7,0,0,0],[5,0,0,7,7,7,7,0],[5,6,0,0,0,0,6,6],[0,7,6,6,8,6,7,7],[0,0,6,0,6,7,6,9],[0,0,6,6,6,7,7,9],[0,0,6,6,6,7,6,7],[5,7,7,0,7,0,0,0]]
TABLEAU = [[0,0,0,7,7,0,0,0],[5,0,0,7,7,7,7,0],[5,6,0,0,0,0,6,6],[0,7,6,6,8,6,7,7],[0,0,6,0,6,7,6,9],[0,0,6,6,6,7,7,9],[0,0,6,6,6,7,6,7],[5,7,7,0,7,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

#             noir        blanc            beige           rose            gris        gris fonce       jaune          orange        rouge      marron     marron fonce     violet        bleu       bleu fonce   vert        vert fonce
COULEURS = [(0, 0, 0),(255, 255, 255),(250, 215, 160),(241, 148, 138),(192, 192, 192),(128, 128, 128),(250, 121, 33),(255, 58, 0),(255, 0, 0),(128, 0, 0),(110, 44, 0),(128, 0, 128),(0, 255, 255),(0, 0, 255),(0, 0, 255),(0, 128, 0)]

def horloge(pixels, color):
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
    #global NEWTABLEAU

    coord = 14
    for k in range(4):
        afficheCiffre = CHIFFRE[afficheHeure[k]]
        x = 0
        y = 0
        for i in range(coord, coord+3):
            for j in range(1, 6):
                TABLEAU[i][j] = afficheCiffre[x][y]
                y = y + 1
            x = x + 1
            y = 0
        if (k == 1):
            coord = coord + 4
            TABLEAU[coord][2] = 6
            TABLEAU[coord][4] = 6
            coord = coord + 2
        else:
            coord = coord + 4
    #print("New: ", NEWTABLEAU, id(NEWTABLEAU))
    #print("Old: ", TABLEAU, id(TABLEAU))
    tableauVersLEDS(pixels, color)



def tableauVersLEDS(pixels, color):
    global TABLEAU
    global COULEURS
    #global NEWTABLEAU
    i = 0
    led = 0
    while i < 31:
        for j in reversed(range(8)):
            #if (NEWTABLEAU[i][j] != 0):
            pixels[led] = COULEURS[TABLEAU[i][j]]
            #elif(TABLEAU[i][j] != 0):
                #print("LED ", str(led), " eteinte")
            #    pixels[led] = (0, 0, 0)
            led = led + 1
        i = i + 1

        for j in range(8):
            #if (NEWTABLEAU[i][j] == 1):
            pixels[led] = COULEURS[TABLEAU[i][j]]
            #elif(TABLEAU[i][j] == 1):
                #print("LED ", str(led), " eteinte")
            #    pixels[led] = (0, 0, 0)
            led = led + 1
        i = i + 1

    pixels.show()

def initTableau():
    print("Reinitialisation du tableau...")
    global TABLEAU
    TABLEAU = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    pixels.fill((0, 0, 0))
    pixels.show()

def getBackground():
    print("Choosing background...")
    num = str(randrange(1,5))
    
    f = open("Backgrounds/" + num + ".txt", "r")

    for idx, line in enumerate(f):
        #Removing \n
        line = line[:-1]
        #Reversing the string
        line = line[::-1]
        for idx2 in range(len(TABLEAU)):
            TABLEAU[idx2][idx] = int(line[idx2])

    f.close()
    
def terminateProcess(signalNumber, frame):
    pixels.fill((0, 0, 0))
    pixels.show()
    exit(0)

if(__name__ == '__main__'):

    signal.signal(signal.SIGTERM, terminateProcess)

    try:
        print("[!] Press ctrl-c to exit")

        #couleurs = [(12, 71, 103), (250, 121, 33), (254, 153, 32), (185, 164, 76), (86, 110, 61)]
        initTableau()
        getBackground()

        changeHeure = 0
        while True:
            minutes = dt.datetime.now().minute
            minutesNow = minutes % 10

            if (minutesNow != changeHeure):
                #print("Affichage de l'heure...")
                #initTableau()
                #time.sleep(1)
                #chooser = random.randrange(0, 4)
                horloge(pixels, (250, 121, 33)) #(12, 71, 103) / (250, 121, 33) / (254, 153, 32) / (185, 164, 76) / (86, 110, 61)
                changeHeure = minutesNow
            time.sleep(1)

    except KeyboardInterrupt:
        terminateProcess(0,0)
