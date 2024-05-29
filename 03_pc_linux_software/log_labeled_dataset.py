import signal
import serial
from datetime import datetime

def exit_close(serial, labeled_dataset_file):
    # Close serial port connection (when finished)
    serial.close()
    labeled_dataset_file.close()

def handle_sigint(sig, frame):
    exit_close(serial, labeled_dataset_file)
    exit(0)  # Exit gracefully
signal.signal(signal.SIGINT, handle_sigint)  # Register the signal handler

def log_file_write_line(line):
    pass

# Create the filename with the current date
filename = f'labeled_dataset_' + datetime.now().strftime("%Y.%m.%d-%Hh%Mm%Ss") + '.csv'
labeled_dataset_file = open(filename, "w")

header_line = f'current,R,G,B\n'
labeled_dataset_file.write(header_line)

# Define serial port settings
port = "/dev/ttyACM0"
timeout = 0.010 # 100ms should be enough

# Open serial port connection
try:
    serial = serial.Serial(port, timeout=timeout)
except serial.SerialException as e:
    print(f"Error connecting to serial port: {e}")
    exit()

r = 0
g = 0
b = 0
rx_new_data = False

while True:
    try:
        # Read data from serial port
        uart_data = serial.readline().decode('utf-8').rstrip()
        if uart_data:
            # sometimes the rx UART values are not ok (like at startup)
            # this try except will skip that case
            try:
                rgb = uart_data.split(',')
                target_current = float(rgb[0])
                r = int(rgb[1])
                g = int(rgb[2])
                b = int(rgb[3])
                rx_new_data = True
            except Exception as e:
                pass

            # target_current must be < 1.0, otherwise the data is wrong and usually happens at startup
            if rx_new_data and target_current < 1.0:
                
                # echo the RGB values to the observer board
                # first byte '2' is command to change LED value
                string_to_send = f'{2},{r},{g},{b}'
                serial.write(bytes(string_to_send, "utf-8"))
                
                # log the data
                string_to_log = f'{target_current:.6f}, {r:3}, {g:3}, {b:3}'
                labeled_dataset_file.write(string_to_log + '\n')
                labeled_dataset_file.flush()
                
                # just for debug
                print(string_to_log)
            
            rx_new_data = False
            
            # reset any bytes on the input buffer
            if serial.in_waiting:
                serial.reset_input_buffer()

    except KeyboardInterrupt:
        break

exit_close(serial, labeled_dataset_file)
