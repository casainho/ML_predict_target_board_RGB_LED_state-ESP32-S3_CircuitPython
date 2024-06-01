import wifi
import busio
import board
import supervisor
import neopixel
import time
from adafruit_ina260 import INA260, Mode, ConversionTime, AveragingCount
import filter
import decision_tree_custom
clf_microcontroller = decision_tree_custom.DecisionTreeCustom()

import mlp_custom

# 0.069850	[   0,   0,   0]
# 0.083289	[   0,   0, 195]
# 0.085641	[   0, 225,   0]
# 0.088599	[ 255,   0,   0]
# 0.099266	[ 255,   0, 195]
# 0.101828	[   0, 225, 195]
# 0.104111	[ 255, 225,   0]
# 0.117829	[ 255, 225, 195]

classes = [
    [   0,   0,   0],
    [   0,   0, 195],
    [   0, 225,   0],
    [ 255,   0,   0],
    [   0, 225, 195],
    [ 255,   0, 195],
    [ 255, 225,   0],
    [ 255, 225, 195]
]

from ulab import numpy as np

weights = [
    np.array([-13.93341374]),  # First array from the output
    np.array([[3.64747954,  2.9748909 ,  2.19930551, -0.18794157,  1.01707484, -3.44739486, -6.49627007, -7.36355271]])  # Second array from the output
]

biases = [
    np.array([3.56570052]),  # First array from the output
    np.array([-22.14459945,  -8.55309862,   1.30376782,  18.06572369, 13.79179861,   8.07800175,  -8.62409213, -19.77643211])  # Second array from the output
]

clf_mlp_custom = mlp_custom.MLP(weights, biases, classes)

x = [0.06, 0.08, 0.084, 0.865, 0.095, 0.100, 0.102]
scale = (1/64.48804207)

import microcontroller

while True:

    for v in x:
        microcontroller.disable_interrupts()
        init_time = time.monotonic_ns()
        _class, number = clf_mlp_custom.predict(np.array([v*scale]))
        final_time = time.monotonic_ns()
        microcontroller.enable_interrupts()
        
        print('processing time clf_mlp_custom.predict: ', (final_time - init_time), 'nano seconds')
        
        print('Predicted class:', _class, 'number:', number, '\n')
    
    print()
    time.sleep(3)



# class RunningMode:
#     USB_PC_DISABLED = 0
#     USB_PC_ENABLED = 1
    
# # running_mode = RunningMode.USB_PC_ENABLED
# running_mode = RunningMode.USB_PC_DISABLED

# if running_mode == RunningMode.USB_PC_DISABLED:
#     print('\nOBSERVER\n')

# # disable wifi to reduce current usage
# wifi.radio.enabled = False

# supervisor.runtime.autoreload = False

# # disable this LED, which should be the RGB LED controlled by the CircuitPyhton supervisor
# supervisor.runtime.rgb_status_brightness = 0

# def list_i2c_devices_addresses(i2c):
#     # find devices I2C 
#     while not i2c.try_lock():
#         pass

#     try:
#         if running_mode == RunningMode.USB_PC_DISABLED:
#             print(f'I2C devices addresses founds: {[hex(device_address) for device_address in i2c.scan()]}')
        
#     finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
#         i2c.unlock()

# # configure INA260 current sensor
# i2c = busio.I2C(board.IO15, board.IO16)
# # list_i2c_devices_addresses(i2c)

# # RED LED at max 255:
# # INA21873 --> 8.72mV
# # Resistor = 0.1 ohm
# # Current = 0.00872 / 0.1 = 87.2mA
# ina226_current_factor = 0.046582

# ina226 = INA260(i2c, address=0x44, ina2xx_id=550, current_factor=ina226_current_factor)
# ina226.averaging_count = AveragingCount.COUNT_1
# ina226.current_conversion_time = ConversionTime.TIME_8_244_ms
# ina226.mode = Mode.TRIGGERED

# # filter_current = filter.FilterLowPass()
# filter_current = filter.FilterMedian()

# # filter settings: read current every 15ms / 66Hz, and get the samples of 0.2 second -- total of 14 samples
# # this values were tested and the results were very good - std: 0.00015 amp
# reading_current_delta_time = 0.015
# reading_current_total_time = 0.200

# # configure UART for communications with the target board
# uart = busio.UART(
#     board.IO10,
#     board.IO9,
#     baudrate = 9600,
#     timeout = 0.010, # 10ms is enough for reading the UART
#     # NOTE: on CircuitPyhton 8.1.0-beta.2, a value of 512 will make the board to reboot if wifi wireless workflow is not connected
#     receiver_buffer_size = 1024)

# # configure the RGB LED
# led_rgb_pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
# led_rgb_pixels[0] = (0, 0, 0)

# if running_mode == RunningMode.USB_PC_ENABLED:
#     import usb_cdc
#     uart_usb = usb_cdc.data
#     # timeout of 10ms should be enough
#     uart_usb.timeout = 0.010
#     uart_usb.write_timeout = 0.010

# def set_rgb_led(r, g, b):
#     led_rgb_pixels[0] = (r, g, b)
    
# def read_target_current():
#     # trigger a new measure
#     ina226.mode = Mode.TRIGGERED
#     return ina226.current / 1000.0

# def read_target_current_filtered():
#     current_value = 0
    
#     # read ADC value, doing the oversampling to reduce the noise
#     reading_current_initial_time = time.monotonic()
#     while True:
#         initial_time = time.monotonic()
        
#         current_value = read_target_current()
#         filter_current.add_new_sample(current_value)
        
#         # stop if adc_reading_total_time has passed
#         current_time = time.monotonic()
#         if current_time > (reading_current_total_time + reading_current_initial_time):
#             break
        
#         # wait _reading_delta_time
#         time_to_sleep = reading_current_delta_time - (current_time - initial_time)
#         # if running_mode == RunningMode.USB_PC_DISABLED:
#         #     print(f'time_to_sleep: {time_to_sleep}')
#         time.sleep(time_to_sleep)
    
#     mean, median, std = filter_current.get_end_stats()
    
#     if running_mode == RunningMode.USB_PC_DISABLED:
#         # print(f'current mean: {mean:.6f}')
#         # print(f'current median: {median:.6f}')
#         # print(f'std: {std}')
#         # print()
#         pass
    
#     return median

# r = 0
# g = 0
# b = 0
# rx_new_rgb_values = False
# tx_new_rgb_values = False
# command = 0

# while True:

#     # when we receive the UART data, the target RGB LED values just changed
#     target_data_uart = uart.read()
#     if target_data_uart is not None:
#         # sometimes the rx UART values are not ok (like at startup)
#         # this try except will skip that case
#         try:
#             data = str(target_data_uart, 'utf-8').split(',')
#             r = int(data[0])
#             g = int(data[1])
#             b = int(data[2])
#             rx_new_rgb_values = True
#         except:
#             pass
        
#         # in the case of new RGB values, send the values to the PC
#         if rx_new_rgb_values:
#             rx_new_rgb_values = False
                        
#             # wait sometime for the RGB LED current to stabilize
#             time.sleep(0.1)
                        
#             target_current = read_target_current_filtered()
#             string_to_send = f'{round(target_current)},{r},{g},{b}\n'
            
#             r, g, b = clf_microcontroller.predict(target_current)
#             set_rgb_led(r, g, b)
#             print(f'predicted values on microcontroller: {r:3}, {g:3}, {b:3}')
            
#             if running_mode == RunningMode.USB_PC_ENABLED:
#                 # send the values to PC    
#                 uart_usb.write(bytes(string_to_send, "utf-8"))
#                 uart_usb.flush()
            
#             elif running_mode == RunningMode.USB_PC_DISABLED:
#                 # print on console
#                 print(f'target_current: {target_current: .6f}')
#                 print(f'r,g,b: {r:3}, {g:3}, {b:3}')    
#                 print()
           
#         # reset the buffer as we should not receive any new data up to now
#         # this helps to keep in syncronization with the target UART communications
#         if uart.in_waiting:
#             uart.reset_input_buffer()
    
#     # when we receive the USB UART data, the target RGB LED values just changed  
#     if running_mode == RunningMode.USB_PC_ENABLED:
#         data_uart_usb = uart_usb.read()
#         if data_uart_usb is not None:
#             # sometimes the rx UART values are not ok (like at startup)
#             # this try except will skip that case
#             tx_new_rgb_values = False
#             try:
#                 data = str(data_uart_usb, 'utf-8').split(',')
#                 command = int(data[0])
#                 r = int(data[1])
#                 g = int(data[2])
#                 b = int(data[3])
#                 tx_new_rgb_values = True
#             except:
#                 pass
            
#             if tx_new_rgb_values:                
#                 # set our RGB LED
#                 if command == 2:
#                     set_rgb_led(r, g, b)
#                 else:
#                     string_to_send = f'{command},{r},{g},{b}'
#                     uart.write(bytes(string_to_send, "utf-8"))

#             # reset the buffer as we should not receive any new data up to now
#             # this helps to keep in syncronization with the PC USB UART communications
#             if uart_usb.in_waiting:
#                 uart_usb.reset_input_buffer()


# import wifi
# import busio
# import board
# import supervisor
# import neopixel
# import time
# from adafruit_ina260 import INA260, Mode, ConversionTime, AveragingCount
# import filter
# import decision_tree_custom
# clf_microcontroller = decision_tree_custom.DecisionTreeCustom()

# class RunningMode:
#     USB_PC_DISABLED = 0
#     USB_PC_ENABLED = 1
    
# # running_mode = RunningMode.USB_PC_ENABLED
# running_mode = RunningMode.USB_PC_DISABLED

# if running_mode == RunningMode.USB_PC_DISABLED:
#     print('\nOBSERVER\n')

# # disable wifi to reduce current usage
# wifi.radio.enabled = False

# supervisor.runtime.autoreload = False

# # disable this LED, which should be the RGB LED controlled by the CircuitPyhton supervisor
# supervisor.runtime.rgb_status_brightness = 0

# def list_i2c_devices_addresses(i2c):
#     # find devices I2C 
#     while not i2c.try_lock():
#         pass

#     try:
#         if running_mode == RunningMode.USB_PC_DISABLED:
#             print(f'I2C devices addresses founds: {[hex(device_address) for device_address in i2c.scan()]}')
        
#     finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
#         i2c.unlock()

# # configure INA260 current sensor
# i2c = busio.I2C(board.IO15, board.IO16)
# # list_i2c_devices_addresses(i2c)

# # RED LED at max 255:
# # INA21873 --> 8.72mV
# # Resistor = 0.1 ohm
# # Current = 0.00872 / 0.1 = 87.2mA
# ina226_current_factor = 0.046582

# ina226 = INA260(i2c, address=0x44, ina2xx_id=550, current_factor=ina226_current_factor)
# ina226.averaging_count = AveragingCount.COUNT_1
# ina226.current_conversion_time = ConversionTime.TIME_8_244_ms
# ina226.mode = Mode.TRIGGERED

# # filter_current = filter.FilterLowPass()
# filter_current = filter.FilterMedian()

# # filter settings: read current every 15ms / 66Hz, and get the samples of 0.2 second -- total of 14 samples
# # this values were tested and the results were very good - std: 0.00015 amp
# reading_current_delta_time = 0.015
# reading_current_total_time = 0.200

# # configure UART for communications with the target board
# uart = busio.UART(
#     board.IO10,
#     board.IO9,
#     baudrate = 9600,
#     timeout = 0.002, # 10ms is enough for reading the UART
#     receiver_buffer_size = 64)

# # configure the RGB LED
# led_rgb_pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
# led_rgb_pixels[0] = (0, 0, 0)

# if running_mode == RunningMode.USB_PC_ENABLED:
#     import usb_cdc
#     uart_usb = usb_cdc.data
#     # timeout of 10ms should be enough
#     uart_usb.timeout = 0.010
#     uart_usb.write_timeout = 0.010

# def set_rgb_led(r, g, b):
#     led_rgb_pixels[0] = (r, g, b)
    
# def read_target_current():
#     # trigger a new measure
#     ina226.mode = Mode.TRIGGERED
#     return ina226.current / 1000.0

# def read_target_current_filtered():
#     current_value = 0
    
#     # read ADC value, doing the oversampling to reduce the noise
#     reading_current_initial_time = time.monotonic()
#     while True:
#         initial_time = time.monotonic()
        
#         current_value = read_target_current()
#         filter_current.add_new_sample(current_value)
        
#         # stop if adc_reading_total_time has passed
#         current_time = time.monotonic()
#         if current_time > (reading_current_total_time + reading_current_initial_time):
#             break
        
#         # wait _reading_delta_time
#         time_to_sleep = reading_current_delta_time - (current_time - initial_time)
#         # if running_mode == RunningMode.USB_PC_DISABLED:
#         #     print(f'time_to_sleep: {time_to_sleep}')
        
#         # because sometimes seems there is a long time measured.....
#         if time_to_sleep > reading_current_delta_time or time_to_sleep < 0:
#             time_to_sleep = reading_current_delta_time
        
#         time.sleep(time_to_sleep)
    
#     mean, median, std = filter_current.get_end_stats()
    
#     if running_mode == RunningMode.USB_PC_DISABLED:
#         # print(f'current mean: {mean:.6f}')
#         # print(f'current median: {median:.6f}')
#         # print(f'std: {std}')
#         # print()
#         pass
    
#     return median

# r = 0
# g = 0
# b = 0
# rx_new_rgb_values = False
# tx_new_rgb_values = False
# command = 0

# previous_rgb_list = [0, 0, 0]
# rgb_equal_counter = 0
# while True:
                        
#     # target_current = read_target_current_filtered()
    
#     # # clf_init_time = time.monotonic()
#     # r, g, b = clf_microcontroller.predict(target_current)
#     # # print(f'processing time microcontroller classifier: {time.monotonic() - clf_init_time}')
    
#     # if [r, g, b] == previous_rgb_list:
#     #     if rgb_equal_counter < 2:
#     #         rgb_equal_counter += 1
#     # else:
#     #     previous_rgb_list = [r, g, b]
#     #     rgb_equal_counter = 0
        
#     # if rgb_equal_counter >= 2:  
#     #     set_rgb_led(r, g, b)
#     #     print(f'{r:3}, {g:3}, {b:3} - {target_current:.6f}')

    
#     # when we receive the UART data, the target RGB LED values just changed
#     target_data_uart = uart.read()
#     if target_data_uart is not None:
#         # sometimes the rx UART values are not ok (like at startup)
#         # this try except will skip that case
#         try:
#             data = str(target_data_uart, 'utf-8').split(',')
#             r_ = int(data[0])
#             g_ = int(data[1])
#             b_ = int(data[2])

#             print(f'{r_:3}, {g_:3}, {b_:3} - rx target')
#         except:
#             pass
           
#         # reset the buffer as we should not receive any new data up to now
#         # this helps to keep in syncronization with the target UART communications
#         if uart.in_waiting:
#             uart.reset_input_buffer()
