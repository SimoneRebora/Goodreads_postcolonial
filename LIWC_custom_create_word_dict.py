from resources.read_files import get_filename

# define LIWC dictionary
print("# Select category dictionary to be converted to word dictionary")
liwc_dict = get_filename("LIWC_custom")
my_input = f'LIWC_custom/{liwc_dict}'

def convert_file(input_filename, output_filename):
    # Use a set to track unique lines
    unique_lines = set()

    with open(input_filename, 'r') as infile:
        for line in infile:
            # Strip the line to remove leading/trailing whitespaces
            line = line.strip()
            # If the line is empty, skip it
            if not line:
                continue
            # Split by the comma and take the first part
            word = line.split(' ,')[0]
            # Form the new line
            new_line = f"{word} ,{word}\n"
            # Add it to the set
            unique_lines.add(new_line)

    # Write the unique lines to the output file
    with open(output_filename, 'w') as outfile:
        for line in unique_lines:
            outfile.write(line)

# Using the function
convert_file(my_input, my_input.replace('.txt', '_words.txt'))
