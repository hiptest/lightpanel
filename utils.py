# -*- coding: utf8

def bound(value, min_val, max_val):
    """ Returns value bound between min and max value.

    >>> bound(0, 1, 2)
    1
    >>> bound(5, 0, 3)
    3
    >>> bound(10, 0, 20)
    10
    """
    return max(min_val, (min(max_val, value)))

def byte_bound(b):
    """ Returns b bound between 0 and 254

    >>> byte_bound(-5)
    0
    >>> byte_bound(100)
    100
    >>> byte_bound(300)
    255
    """
    return int(bound(b, 0, 255))

def fade_color(color, fade):
    """
    >>> fade_color([255, 255, 255], 1) == bytearray(b'\xff\xff\xff')
    True

    >>> fade_color([255, 255, 255], 0.5) == bytearray(b'\x7f\x7f\x7f')
    True

    >>> fade_color([255, 255, 255], 0) == bytearray(3)
    True

    >>> fade_color([255, 255, 255], 2) == bytearray(b'\xff\xff\xff')
    True
    """
    pixels = bytearray(3)

    for i in range(0, 3):
        try:
            pixels[i] = byte_bound(color[i] * fade)
        except:
            pass

    return pixels
