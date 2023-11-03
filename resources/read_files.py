import os

def get_filename(my_directory):

    # Fetch filenames from the folder
    files = [f for f in os.listdir(my_directory) if os.path.isfile(os.path.join(my_directory, f))]

    # If there are no files, inform the user and exit
    if not files:
        print("The folder does not contain any files.")
        return

    # Display files and prompt user to choose one
    print("Here are the files in the folder:")
    for index, file in enumerate(files, 1):
        print(f"{index}. {file}")

    while True:
        try:
            choice = int(input("Select the number of the file you want to work with: "))

            # Check if the choice is valid
            if 1 <= choice <= len(files):
                selected_file = files[choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("Please enter a valid number.")

    # Assign the filename to a variable
    chosen_filename = selected_file
    print(f"You have selected: {chosen_filename}")
    return(chosen_filename)
