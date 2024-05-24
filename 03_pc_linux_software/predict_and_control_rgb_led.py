import signal
import serial
import pickle

# Load the classifier later
with open('classifier.pkl', 'rb') as f:
    clf = pickle.load(f)

def handle_sigint(sig, frame):
    exit(0)  # Exit gracefully
signal.signal(signal.SIGINT, handle_sigint)  # Register the signal handler

def log_file_write_line(line):
    pass

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
                rx_new_data = True
            except Exception as e:
                pass

            # target_current must be < 1.0, otherwise the data is wrong and usually happens at startup
            if rx_new_data and target_current < 1.0:
                
                prediction = clf.predict([[target_current]])
                rgb = prediction[0].split(' ')
                
                r = int(float(rgb[0]))
                g = int(float(rgb[1]))
                b = int(float(rgb[2]))
                
                print(r, g, b)
                
                # echo the RGB values to the observer board
                # first byte '2' is command to change LED value
                string_to_send = f'{2},{r},{g},{b}'
                serial.write(bytes(string_to_send, "utf-8"))
            
            rx_new_data = False
            
            # reset any bytes on the input buffer
            if serial.in_waiting:
                serial.reset_input_buffer()

    except KeyboardInterrupt:
        break

