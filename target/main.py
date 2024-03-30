# Set training_mode to False to run in regular mode
training_mode = True

if training_mode:
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

if training_mode:
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
rgb_percentage = 1.0

# each RGB color will be set with 0, 0.5 or 1, relative to
rgb_random_sequence = [0, int(127 * rgb_percentage), int(255 * rgb_percentage)]

r_random_previous = 0
g_random_previous = 0
b_random_previous = 0

while True:
    # get RGB random values and set the RGB LED
    r, g, b = get_rgb_random()
    set_rgb_led(r, g, b)
    
    if not training_mode:
        # give time so users can have time to visualize RGB LED color
        time.sleep(1)
        
    else:
        # now communicate the current RGB values to the observer board
        uart.write(bytes(f'{r},{g},{b}', "utf-8"))
    
        # give time for observer processing time before repeat
        time.sleep(0.500)
        
