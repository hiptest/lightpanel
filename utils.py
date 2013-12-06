# -*- coding: utf8

def bound(n, min_val, max_val):
    return max(min_val, (min(max_val, n)))

def byte_bound(b):
    return int(bound(b, 0, 254))

def fade_color(color, fade):
    pixels = bytearray(3)

    for i in range(0, 3):
        try:
            pixels[i] = byte_bound(color[i] * fade)
        except:
            pass

    return pixels
