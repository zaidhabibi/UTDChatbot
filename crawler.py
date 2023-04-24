import os

input_folder = 'website data'  # Folder containing input .txt files
output_file = 'combined.txt'  # Output .txt file

# Get a list of all .txt files in the input folder
input_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.txt')]

# Open output file in write mode
with open(output_file, 'w', encoding='utf-8') as outfile:
    for input_file in input_files:
        # Check if file exists and is a .txt file
        if os.path.isfile(input_file) and input_file.endswith('.txt'):
            # Open input file in read mode
            with open(input_file, 'r', encoding='utf-8') as infile:
                # Read the content of input file
                content = infile.read()
                # Write content to the output file
                outfile.write(content)
                # Add a newline to separate content from different input files
                outfile.write('\n')
        else:
            print(f"Skipping: {input_file} (not a valid .txt file or does not exist)")
