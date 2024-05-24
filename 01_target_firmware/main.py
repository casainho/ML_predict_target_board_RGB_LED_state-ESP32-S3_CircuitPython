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

print('\nTARGET\n')

r_random_sequence = [
    0,
    255
]

g_random_sequence = [
    0,
    225
]

b_random_sequence = [
    0,
    195
]

# configure UART for communications with observer board
uart = busio.UART(
    board.IO10,
    board.IO9,
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
    rgb_index = [0, 0, 0]

    for i in [0, 1, 2]:
        index = random.randint(0, 1)
        rgb_index[i] = index
            
    r = r_random_sequence[rgb_index[0]]
    g = g_random_sequence[rgb_index[1]]
    b = b_random_sequence[rgb_index[2]]
 
    return r, g, b

def read_uart_set_rgb_values():
    target_data_uart = uart.read()
    if target_data_uart is not None:
        # sometimes the rx UART values are not ok (like at startup)
        # this try except will skip that case
        try:
            data = str(target_data_uart, 'utf-8').split(',')
            command = int(data[0])
            r = int(data[1])
            g = int(data[2])
            b = int(data[3])
            return command, r, g, b
        except:
            pass
        
        if uart.in_waiting:
            uart.reset_input_buffer()
        
    return None, None, None, None

r = 0
g = 0
b = 0
r_previous = 0
g_previous = 0
b_previous = 0
use_random_rgb = True
while True:
    # check if RGB values were set by the host
    command, new_r, new_g, new_b = read_uart_set_rgb_values()
    if command == 1:
        use_random_rgb = False
        r = new_r
        g = new_g
        b = new_b
    elif command == 0:
        use_random_rgb = True
    else:
        # do nothing, just keep the previous RGB values
        pass       
    
    if use_random_rgb:
        # avoid repetition
        while r == r_previous and g == g_previous and b == b_previous:
            r, g, b = get_rgb_random()
            
        r_previous = r
        g_previous = g
        b_previous = b
            
    set_rgb_led(r, g, b)

    # now communicate the current RGB values to the observer board
    string_to_send = f'{r},{g},{b}'
    uart.write(bytes(string_to_send, "utf-8"))
    print(string_to_send)

    # delay time for processing on the observer and PC
    time.sleep(2.5)
