import signal
import csv

def close_files():
    file_dataset.close()
    file_01.close()

def handle_sigint(sig, frame):
    close_files()
    exit(0)  # Exit gracefully
signal.signal(signal.SIGINT, handle_sigint)  # Register the signal handler

# open datset file
filename_in = './labeled_dataset_2024.05.24-03h39m42s.csv'
file_dataset = open(filename_in, "r")

filename_out = './01.csv'
file_01 = open(filename_out, "w")

unique_combinations_rgb = []

print("Start processing file:", filename_in)
print()

while True:
    try:
        # add R G B values collumn
        
        for index, line in enumerate(file_dataset):
        
            # first line is the header
            if index == 0:
                data = line.strip().split(sep=',')
                new_data_line = f'{data[0]:6},   R    G    B\n'
                file_01.writelines([new_data_line])
                continue
            
            data = line.strip().split(sep=',')
            new_data_line = f'{data[0]:6},{data[1]:3} {data[2]:3} {data[3]:3}\n'
            file_01.writelines([new_data_line])
            
        file_dataset.close()
        file_01.close()
           
           
        # now order de table by the current value, ascending
        input_file = './01.csv'
        output_file = './labeled_dataset_2024.05.24-03h39m42s-rgb_combinations_labeled_ordered.csv'
        
        with open(input_file, 'r') as csvfile:
            reader = csv.reader(csvfile)

            # Read the header row separately
            header = next(reader)
    
            # Read all rows into a list
            data = list(reader)

        # Sort the data by the first float column (assuming it's numeric)
        data.sort(key=lambda row: float(row[0]))

        # Combine the header and sorted data
        sorted_data = [header] + data

        # Open the output file for writing
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the sorted data back to the CSV file
            writer.writerows(sorted_data)
            
        break
    
    except KeyboardInterrupt:
        break

close_files()
