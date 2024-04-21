import wifi
import board
import analogio
import supervisor
import busio
import neopixel
import time
from boot import RunningMode
from boot import running_mode

# disable wifi to reduce current usage
wifi.radio.enabled = False

supervisor.runtime.autoreload = False

# disable this LED, which should be the RGB LED controlled by the CircuitPyhton supervisor
supervisor.runtime.rgb_status_brightness = 0

# ADC pin - board pin 8
adc_pin = board.IO3
adc = analogio.AnalogIn(adc_pin)

# filter settings: read ADC every 5ms, and average the samples of 2 seconds
adc_reading_delta_time = 0.005
adc_reading_total_time = 2.000

# a low pass filter
adc_reading_filter_coeficient = 0.01
adc_value_filtered_value = adc.value

# resistor value to measure the observed target current
resistor_value = 10

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

if running_mode ==  RunningMode.USB_PC_ENABLED:
    import usb_cdc
    uart_usb = usb_cdc.data
    # timeout of 10ms should be enough
    uart_usb.timeout = 0.010
    uart_usb.write_timeout = 0.010

def set_rgb_led(r, g, b):
    led_rgb_pixels[0] = (r, g, b)

def read_target_current():
    global adc_value_filtered_value
    
    # read ADC value, doing the oversampling to reduce the noise
    adc_sum = 0
    adc_sum_counter = 0
    read_current_initial_time = time.monotonic()
    while True:
        initial_time = time.monotonic()
        
        # read the ADC value and accumulate it
        adc_sum += adc.value
        adc_sum_counter += 1
        
        # stop if adc_reading_total_time has passed
        current_time = time.monotonic()
        if current_time > (adc_reading_total_time + read_current_initial_time):
            break
        
        # wait adc_reading_delta_time
        time_to_sleep = adc_reading_delta_time - (current_time - initial_time)
        time.sleep(time_to_sleep / 1000)
    
       
    adc_value_average = adc_sum / adc_sum_counter
    
    adc_value_filtered_value = (adc_value_filtered_value * adc_reading_filter_coeficient) + (adc_value_average * (1.0 - adc_reading_filter_coeficient))
    
    # calculate the target current
    target_current = (adc_value_filtered_value / 65535 * adc.reference_voltage) / resistor_value
    return target_current


adc_sum = 0
adc_reference_voltage = 0
r = 0
g = 0
b = 0
rx_new_rgb_values = False
tx_new_rgb_values = False

while True:
    # when we receive the UART data, the target RGB LED values just changed
    target_data_uart = uart.read()
    if target_data_uart is not None:
        # sometimes the rx UART values are not ok (like at startup)
        # this try except will skip that case
        try:
            rgb = str(target_data_uart, 'utf-8').split(',')
            r = int(rgb[0])
            g = int(rgb[1])
            b = int(rgb[2])
            rx_new_rgb_values = True
        except:
            pass
        
        # in the case of new RGB values, send the values to the PC
        if rx_new_rgb_values:
            rx_new_rgb_values = False
                        
            # wait sometime for the RGB LED current to stabilize
            time.sleep(2.5)
                        
            target_current = read_target_current()
            string_to_send = f'{round(target_current, 6)},{r},{g},{b}\n'
            
            if running_mode == RunningMode.USB_PC_ENABLED:    
                # send the values to PC    
                uart_usb.write(bytes(string_to_send, "utf-8"))
                uart_usb.flush()
            
            elif running_mode ==  RunningMode.USB_PC_DISABLED:
                # print on console
                print(target_current)
                print(f'{r},{g},{b}\n')
                print()
           
        # reset the buffer as we should not receive any new data up to now
        # this helps to keep in syncronization with the target UART communications
        if uart.in_waiting:
            uart.reset_input_buffer()
    
    # when we receive the USB UART data, the target RGB LED values just changed  
    if running_mode == RunningMode.USB_PC_ENABLED:
        data_uart_usb = uart_usb.read()
        if data_uart_usb is not None:
            # sometimes the rx UART values are not ok (like at startup)
            # this try except will skip that case
            try:
                rgb = str(data_uart_usb, 'utf-8').split(',')
                r = int(rgb[0])
                g = int(rgb[1])
                b = int(rgb[2])
                tx_new_rgb_values = True
            except:
                pass
            
            # set our RGB LED
            if tx_new_rgb_values:
                tx_new_rgb_values = False
                set_rgb_led(r, g, b)
                
            # reset the buffer as we should not receive any new data up to now
            # this helps to keep in syncronization with the PC USB UART communications
            if uart_usb.in_waiting:
                uart_usb.reset_input_buffer()
