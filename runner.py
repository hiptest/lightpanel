#!/usr/bin/python

import time
import colors
import writer
import threading

import signal
import sys

from config import LEDS, CHECK_INTERVAL, BLINK_INTERVAL

STATIC = 0
BLINK = 1

strip = [(STATIC, colors.BLACK)] * len(LEDS)

def update_strip():
    global strip

    while True:
        for index, led in enumerate(LEDS):
            if led is None:
                strip[index] = (STATIC, colors.BLACK)
                continue

            try:
                status = led.check()
                color = led.success_color if status else led.failure_color
                strip[index] = (STATIC, color)

            except:               
                strip[index] = (BLINK, colors.ORANGE)

        time.sleep(CHECK_INTERVAL)

def display():
    global strip

    while True:
        on_strip = [x[1] for x in strip]
        off_strip = [x[1] if x[0] == STATIC else colors.BLACK 
                    for x in strip]

        writer.write(on_strip)
        time.sleep(BLINK_INTERVAL)
        writer.write(off_strip)
        time.sleep(BLINK_INTERVAL)

threads = [threading.Thread(None, update_strip, None, (), {}),
           threading.Thread(None, display, None, (), {})]

def on_kill(signal, frame):
    print 'Caught SIGTERM'
    [th._Thread__stop() for th in threads]
    writer.all_off()

[th.start() for th in threads]
signal.signal(signal.SIGTERM, on_kill)
signal.pause()
