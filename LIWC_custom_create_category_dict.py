import csv
from resources.read_files import get_filename

# define LIWC dictionary
print("# Select RAW dictionary to be converted to category dictionary")
liwc_dict = get_filename("LIWC_custom")
input_file = f'LIWC_custom/{liwc_dict}'

# Read the CSV file
with open(input_file, 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Get the header which contains category names
    header = next(csv_reader)

    # To store the output in the desired format
    output_data = []

    # Iterate through each row in the csv file
    for row in csv_reader:
        for i, word in enumerate(row):
            # Check if the cell is not empty
            if word:
                output_data.append(f'{word} ,{header[i]}')

# remove duplicated entries
output_data = set(output_data)

output_file = input_file.replace("_RAW.csv", ".txt")

# Write the output data to a txt file
with open(output_file, 'w') as txt_file:
    for line in output_data:
        txt_file.write(line + '\n')

print(f"Conversion complete! Check {output_file} for the output.")
