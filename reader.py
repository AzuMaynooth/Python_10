import sys
import csv
import os
import json
import pickle

# Abstract class with common interfaz to read and save files
class FileHandler:
    def read(self, file_path):
        raise NotImplementedError

    def write(self, file_path, data):
        raise NotImplementedError

    def print_content(self, data):
        for row in data:
            print(",".join(map(str, row)))

# Heritage from FileHandler to csv files
class CSVHandler(FileHandler):
    def read(self, file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            return list(reader)

    def write(self, file_path, data):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

# Heritage from FileHandler to json files
class JSONHandler(FileHandler):
    def read(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def write(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file)

# PickleReader is a subclass from FileReader read and save file in Pickle format
# Pickle is module to serialization, allowing convert object in binary and vice-versa

class PickleHandler(FileHandler):
    def read(self, file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)

    def write(self, file_path, data):
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)

# base on type of file apply funtions
def get_file_handler(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == '.csv':
        return CSVHandler()
    elif ext == '.json':
        return JSONHandler()
    elif ext == '.pickle':
        return PickleHandler()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def display_directory_contents(directory):
    print(f"Error: File not found. Files in the directory '{directory}':")


def apply_changes(data, changes):
    for change in changes:
        try:
            x, y, value = change.split(',')
            x = int(x)
            y = int(y)
            data[y][x] = value
        except (ValueError, IndexError):
            print(f"Invalid change format or index out of range: {change}")

def main():
    if len(sys.argv) < 4:
        print("Usage: reader.py <src> <dst> <change1> <change2> ...")
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    if not os.path.isfile(src):
        display_directory_contents(os.path.dirname(src) or '.')
        sys.exit(1)

    try:
        src_handler = get_file_handler(src)
        dst_handler = get_file_handler(dst)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Read original data
    data = src_handler.read(src)
    #print("\nOriginal content of the file:")
    #src_handler.print_content(data)

    # Apply changes
    apply_changes(data, changes)
    #print("\nModified content of the file:")
    #dst_handler.print_content(data)

    # Write a json file with changes
    dst_handler.write(dst, data)
    #print(f"\nModified file saved to '{dst}'.")
    #print(json.dumps(data, indent=4))

if __name__ == "__main__":
    main()
