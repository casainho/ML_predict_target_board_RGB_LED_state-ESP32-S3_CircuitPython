import signal

def exit_close(labeled_dataset_file, labeled_dataset_file_rgb_combinations_labeled):
    labeled_dataset_file.close()
    labeled_dataset_file_rgb_combinations_labeled.close()

def handle_sigint(sig, frame):
    exit_close()
    exit(0)  # Exit gracefully
signal.signal(signal.SIGINT, handle_sigint)  # Register the signal handler

# open datset file
filename_in = 'labeled_dataset.csv'
labeled_dataset_file = open(filename_in, "r")

filename_out = 'labeled_dataset-rgb_combinations_labeled.csv'
labeled_dataset_file_rgb_combinations_labeled = open(filename_out, "w")

unique_combinations_rgb = []

print("Start processing file:", filename_in)
print()

while True:
    try:
        for index, line in enumerate(labeled_dataset_file):
        
            # first line is the header
            if index == 0:
                line = line.strip()
                line += ',rgb unique combination\n' 
                labeled_dataset_file_rgb_combinations_labeled.writelines([line])
                continue
            
            # get the values in a list
            data = line.strip().split(sep=',')
            # make a new list with RGB values only
            data_rgb = data[1:].copy()
            
            # append RGB values list to unique_combinations_rgb list, if not exist already
            if data_rgb not in unique_combinations_rgb:
                unique_combinations_rgb.append(data_rgb)
                
            # find the index of RGB values list in unique_combinations_rgb list
            index = unique_combinations_rgb.index(data_rgb)
            
            # write the new data line with the unique_combinations_rgb label
            new_data_line = ''
            for value in data:
                new_data_line += f'{value},'
                
            new_data_line += str(index)
            new_data_line += '\n'
            labeled_dataset_file_rgb_combinations_labeled.writelines([new_data_line])

        print("End of processing file.\nWrote new file:", filename_out)
        break

    except KeyboardInterrupt:
        break

exit_close(labeled_dataset_file, labeled_dataset_file_rgb_combinations_labeled)
