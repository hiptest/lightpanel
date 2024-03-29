# -*- coding: utf8

import colors
import config

PIXEL_SIZE = 3
spidev = file('/dev/spidev0.0', "wb")

def all_off():
    write ([colors.BLACK] * config.LEDS_COUNT)

def all_on():
    write ([colors.WHITE] * config.LEDS_COUNT)

def write(d):
    pixel_output = bytearray(len(d) * PIXEL_SIZE + 3)
    for led, color in enumerate(d):
        pixel_output[led*PIXEL_SIZE:] = color

    spidev.write(pixel_output)
    spidev.flush()
