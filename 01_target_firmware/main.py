import busio
import time
import supervisor
import wifi
import board
import neopixel
import random

import supervisor
supervisor.runtime.autoreload = False

wifi.radio.enabled = False

# configure UART for communications with observer board
uart = busio.UART(
    board.IO10,
    None,
    baudrate = 9600,
    timeout = 0.01, # 10ms is enough for writing to the UART
    # NOTE: on CircuitPyhton 8.1.0-beta.2, a value of 512 will make the board to reboot if wifi wireless workflow is not connected
    receiver_buffer_size = 1024)

# configure the RGB LED
led_rgb_pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
led_rgb_pixels[0] = (0, 0, 0)

def set_rgb_led(r, g, b):
    led_rgb_pixels[0] = (r, g, b)

def get_rgb_random():
    global r_random_previous
    global g_random_previous
    global b_random_previous
    
    # max tries to get a new random
    random_counter = 5
    
    # we want a new different random value
    while random_counter > 0:
        r = random.choice(rgb_random_sequence)
        g = random.choice(rgb_random_sequence)
        b = random.choice(rgb_random_sequence)
        
        # check if random is different from previous
        if r != r_random_previous or g == g_random_previous or b == b_random_previous:
            break
        
        r_random_previous = r
        g_random_previous = g
        b_random_previous = b
        random_counter -= 1
    
    return r, g, b

# percentage of RGB value, 1.0 will be full 255 value on each RGB
rgb_percentage = 0.80

# each RGB color will be set with one of each values
rgb_random_sequence = [
    0,
    int(255 * 0.50 * rgb_percentage),
    int(255 * 0.80 * rgb_percentage)
]

r_random_previous = 0
g_random_previous = 0
b_random_previous = 0

while True:
    # get RGB random values and set the RGB LED
    r, g, b = get_rgb_random()
    set_rgb_led(r, g, b)
    
    # now communicate the current RGB values to the observer board
    uart.write(bytes(f'{r},{g},{b}', "utf-8"))

    # delay time for processing on the observer and PC
    time.sleep(1)
        
