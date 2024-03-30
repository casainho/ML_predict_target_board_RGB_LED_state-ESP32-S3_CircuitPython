import wifi
import board
import analogio
import supervisor
import busio
import neopixel
import time

wifi.radio.enabled = False

supervisor.runtime.autoreload = False

# 1. Read from UART the other board current RGB LED state
# 2. Read ADC value, relative to the other board current usage
# 3. Send the ADC value and RGB LED state to PC (USB connection)

# ADC pin - board pin 8
adc_pin = board.IO3

# a value between 1 and 1000
adc_oversampling = 200

# resistor value to measure the observed target current
resistor_value = 3.33


# configure UART for communications with the target board
uart = busio.UART(
    None,
    board.IO9,
    baudrate = 9600,
    timeout = 0.010, # 10ms is enough for reading the UART
    # NOTE: on CircuitPyhton 8.1.0-beta.2, a value of 512 will make the board to reboot if wifi wireless workflow is not connected
    receiver_buffer_size = 1024)

# configure the RGB LED
led_rgb_pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
led_rgb_pixels[0] = (0, 0, 0)

def set_rgb_led(r, g, b):
    led_rgb_pixels[0] = (r, g, b)

def read_target_current():
    global adc_reference_voltage
    global adc_oversampling
    
    # read ADC value, doing the oversampling to reduce the noise
    adc_sum = 0
    with analogio.AnalogIn(adc_pin) as adc:
        adc_reference_voltage = adc.reference_voltage
        for i in range(adc_oversampling):
           adc_sum += adc.value
        
    adc_value = adc_sum / adc_oversampling
    
    # calculate the observed target current
    target_current = (adc_value / 65535 * adc_reference_voltage) / resistor_value
    return target_current

adc_sum = 0
adc_reference_voltage = 0
r = 0
g = 0
b = 0
new_rgb_values = False

while True:
    
    # when we receive the UART data, the target RGB LED values just changed
    uart_data = uart.read()
    if uart_data is not None:
        # sometimes the rx UART values are not ok (like at startup)
        # this try except will skip that case
        try:
            rgb = str(uart_data, 'utf-8').split(',')
            r = int(rgb[0])
            g = int(rgb[1])
            b = int(rgb[2])
            new_rgb_values = True
        except:
            # print('UART target rx error')
            pass
        
        # in the case of new RGB values, update the RGB LED and send the values to the PC
        if new_rgb_values:
            new_rgb_values = False
            
            # wait sometime for the RGB LED current to stabilize
            time.sleep(0.01)
            
            # set our RGB LED to replicate the target one
            set_rgb_led(r, g, b)
            
            # send the values to PC
            print(f'{round(read_target_current(), 6)},{r},{g},{b}')
           
        # reset the buffer as we should not receive any new data up to now
        # this helps to keep in syncronization with the target UART communications
        uart.reset_input_buffer()

