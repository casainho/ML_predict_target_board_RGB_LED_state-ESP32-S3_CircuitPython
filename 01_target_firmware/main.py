import busio
import time
import supervisor
import wifi
import board
import neopixel
import random

import supervisor
supervisor.runtime.autoreload = False
supervisor.runtime.rgb_status_brightness = 0

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
        r = random.choice(r_random_sequence)
        g = random.choice(g_random_sequence)
        b = random.choice(b_random_sequence)
        
        # check if random is different from previous
        if r != r_random_previous or g == g_random_previous or b == b_random_previous:
            break
        
        r_random_previous = r
        g_random_previous = g
        b_random_previous = b
        random_counter -= 1
        
    value = random.choice(range(3))
    if value == 0: r = 0
    elif value == 1: g = 0
    else: b = 0

    return r, g, b

#########
# Each RGB color will be set with one of each values

r_random_sequence = [
    63,
    127
]

g_random_sequence = [
    42,
    106
]

b_random_sequence = [
    21,
    85
]

r_random_previous = 0
g_random_previous = 0
b_random_previous = 0

set_rgb_led(0, 0, 0)

while True:
    # get RGB random values and set the RGB LED
    r, g, b = get_rgb_random()
    set_rgb_led(r, g, b)
    
    # now communicate the current RGB values to the observer board
    string_to_send = f'{r},{g},{b}'
    uart.write(bytes(string_to_send, "utf-8"))
    print(string_to_send)

    # delay time for processing on the observer and PC
    time.sleep(5)
