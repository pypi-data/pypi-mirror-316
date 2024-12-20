import os

def read_list_from_file(file_path):
    with open(file_path, 'r') as file: 
        content = file.readlines()
        data_list = [eval(line.strip()) for line in content] # Strip any leading/trailing whitespace from each line and convert to proper data type
    return data_list

def write_list_to_file(file_path, data):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)    
    # Write data to the file
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + '\n')

def append_list_to_file(file_path, data):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)    
    # Append data to the file
    with open(file_path, 'a') as file:
        for item in data:
            file.write(str(item) + '\n')