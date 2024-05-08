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


r_random_sequence = [
    45,
    85
]

g_random_sequence = [
    120,
    170,
]

b_random_sequence = [
    215,
    255
]

rgb_sequence_lists_index =[
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]]

# https://g.co/gemini/share/174b648d17ed
# LCG algorithm
def random_lcg(seed, max_value, repeat_pattern):
  """Generates a pseudo-random sequence of 1, 2, or 3 with a repeating pattern of 'repeat_pattern' values.

  Args:
      seed: An initial value to influence the sequence.
      max_value: The maximum value (exclusive) for the generated sequence (e.g., 3 for 1, 2, 3).
      repeat_pattern: The length of the repeating pattern.

  Returns:
      A single integer (1, 2, or 3) based on the current position in the sequence.
  """
  state = seed
  while True:
    new_state = (state * 1103515245 + 12345) % 2**31
    value = new_state % max_value + 1
    state = new_state
    yield value % repeat_pattern + 1  # Ensure value falls within repeat_pattern

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

random_generator = random_lcg(
    4, # seed value
    len(rgb_sequence_lists_index), # number of lists
    30) # repeat after 30

def get_rgb_random():
    
    # get a random element from rgb_sequence_lists_index
    # index = next(random_generator) - 2
    # rgb_sequence_lists_index[index][0]
        
    index = random.randint(0, len(rgb_sequence_lists_index))
        
    r = r_random_sequence[rgb_sequence_lists_index[index][0]]
    g = g_random_sequence[rgb_sequence_lists_index[index][1]]
    b = b_random_sequence[rgb_sequence_lists_index[index][2]]
        
    return r, g, b

while True:
    # get RGB random values and set the RGB LED
    r, g, b = get_rgb_random()
    set_rgb_led(r, g, b)

    # now communicate the current RGB values to the observer board
    string_to_send = f'{r},{g},{b}'
    uart.write(bytes(string_to_send, "utf-8"))
    print(string_to_send)

    # delay time for processing on the observer and PC
    time.sleep(10.0)
    