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


TABLEAU = []

#             noir        blanc          jaune          orange        rouge      violet        bleu       bleu fonce     vert
COULEURS = [(0, 0, 0),(55, 55, 55),(250, 121, 33),(155, 58, 0),(155, 10, 10),(128, 0, 128),(0, 155, 155),(0, 0, 155),(0, 128, 0)]


def fire():
    for ligne in range(32):
        for col in range(8):
            if(col == 7):
                alea = randrange(100)
                if(alea < 40):
                    TABLEAU[ligne][col] = 3
                else:
                    TABLEAU[ligne][col] = 2

            if(col == 6):
                alea = randrange(100)
                if(alea < 20):
                    TABLEAU[ligne][col] = 4
                elif(alea >= 20 and alea < 50):
                    TABLEAU[ligne][col] = 3
                else:
                    TABLEAU[ligne][col] = 2
            
            if(col == 5):
                alea = randrange(100)
                if(alea < 40):
                    TABLEAU[ligne][col] = 4
                elif(alea >= 40 and alea < 70):
                    TABLEAU[ligne][col] = 3
                else:
                    TABLEAU[ligne][col] = 2

            if(col == 4):
                alea = randrange(100)
                if(TABLEAU[ligne][col+1] == 4):
                    if(alea < 40):
                        TABLEAU[ligne][col] = 0
                    else:
                        TABLEAU[ligne][col] = 4
                elif(TABLEAU[ligne][col+1] == 3):
                    if(alea < 50):
                        TABLEAU[ligne][col] = 4
                    else:
                        TABLEAU[ligne][col] = 3
                else:
                    TABLEAU[ligne][col] = 0
            
            if(col == 3):
                alea = randrange(100)
                if(TABLEAU[ligne][col+1] == 4):
                    if(alea < 50):
                        TABLEAU[ligne][col] = 0
                    else:
                        TABLEAU[ligne][col] = 4
                elif(TABLEAU[ligne][col+1] == 3):
                    if(alea < 60):
                        TABLEAU[ligne][col] = 4
                    else:
                        TABLEAU[ligne][col] = 3
                else:
                    TABLEAU[ligne][col] = 0

            if(col == 2):
                alea = randrange(100)
                if(TABLEAU[ligne][col+1] == 4):
                    if(alea < 60):
                        TABLEAU[ligne][col] = 0
                    else:
                        TABLEAU[ligne][col] = 4
                elif(TABLEAU[ligne][col+1] == 3):
                    if(alea < 70):
                        TABLEAU[ligne][col] = 4
                    else:
                        TABLEAU[ligne][col] = 3
                else:
                    TABLEAU[ligne][col] = 0

            if(col == 1):
                alea = randrange(100)
                if(TABLEAU[ligne][col+1] == 4):
                    if(alea < 70):
                        TABLEAU[ligne][col] = 0
                    else:
                        TABLEAU[ligne][col] = 4
                elif(TABLEAU[ligne][col+1] == 3):
                    if(alea < 80):
                        TABLEAU[ligne][col] = 4
                    else:
                        TABLEAU[ligne][col] = 3
                else:
                    TABLEAU[ligne][col] = 0

            if(col == 0):
                alea = randrange(100)
                if(TABLEAU[ligne][col+1] == 4):
                    if(alea < 80):
                        TABLEAU[ligne][col] = 0
                    else:
                        TABLEAU[ligne][col] = 4
                elif(TABLEAU[ligne][col+1] == 3):
                    if(alea < 90):
                        TABLEAU[ligne][col] = 4
                    else:
                        TABLEAU[ligne][col] = 3
                else:
                    TABLEAU[ligne][col] = 0


def tableauVersLEDS():
    global TABLEAU
    global COULEURS

    i = 0
    led = 0
    while i < 31:
        for j in reversed(range(8)):
            pixels[led] = COULEURS[TABLEAU[i][j]]
            led = led + 1
        i = i + 1

        for j in range(8):
            pixels[led] = COULEURS[TABLEAU[i][j]]
            led = led + 1
        i = i + 1

    pixels.show()


def initTableau():
    print("Reinitialisation du tableau...")
    global TABLEAU

    TABLEAU = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

    
    pixels.fill((0, 0, 0))
    pixels.show()


def terminateProcess(signalNumber, frame):
    pixels.fill((0, 0, 0))
    pixels.show()
    exit(0)


if(__name__ == '__main__'):

    signal.signal(signal.SIGTERM, terminateProcess)

    try:
        print("[!] Press ctrl-c to exit")

        initTableau()

        changeHeure = 0
        while True:
            fire()
            tableauVersLEDS()
            time.sleep(0.1)

    except KeyboardInterrupt:
        terminateProcess(0,0)
