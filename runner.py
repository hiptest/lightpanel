#!/usr/bin/python
# -*- coding: utf8

import time
import colors
import writer
import threading

import signal
import sys

from config import LEDS_COUNT, LEDS_CONFIG, CHECK_INTERVAL, BLINK_INTERVAL, FADE
from jenkins import JeanXV
from response import Response

from utils import byte_bound, fade_color

strip = [(colors.STATIC, colors.BLUE)] * LEDS_COUNT

# Build LEDS array from LEDS_CONFIG
def build_leds_from_config():
    leds = [None] * LEDS_COUNT
    for number, led_config in LEDS_CONFIG.iteritems():
        led_class = globals()[led_config['class_name']]
        args = led_config.get('args', [])
        kwargs = led_config.get('kwargs', {})
        leds[number] = led_class(*args, **kwargs)
    return leds

LEDS = build_leds_from_config()


def update_strip():
    global strip

    while True:
        for index, led in enumerate(LEDS):
            if led is None:
                strip[index] = (colors.STATIC, colors.BLACK)
                continue

            try:
                led.check()
                strip[index] = led.status
                led.notify()

            except Exception as e:
                strip[index] = (colors.BLINK, colors.ORANGERED)
                print '-----------------------------'
                print 'Error on job #%s' % index
                print e

        #print [(x[0], '%s.%s.%s' % (x[1][0], x[1][1], x[1][2])) for x in strip]
        time.sleep(CHECK_INTERVAL)

def display():
    global strip

    modifier = 0.01
    color_filter = 0

    while True:
        computed_strip = []
        if color_filter < 0 or color_filter > 1:
            modifier = -modifier

        for led in strip:
            if led[0] == colors.STATIC:
                computed_strip.append(led[1])
                continue

            if led[0] == colors.BLINK:
                if modifier > 0:
                    computed_strip.append(led[1])
                else:
                    computed_strip.append(colors.BLACK)
                continue

            computed_strip.append(fade_color(led[1], color_filter))

        color_filter += modifier
        writer.write([fade_color(x, FADE) for x in computed_strip])
        time.sleep(0.01)


threads = [threading.Thread(None, update_strip, None, (), {}),
           threading.Thread(None, display, None, (), {})]

def on_kill(signal, frame):
    print 'Caught SIGTERM'
    [th._Thread__stop() for th in threads]
    writer.all_off()

[th.start() for th in threads]
signal.signal(signal.SIGTERM, on_kill)
signal.pause()


