import os
import sys

def process_file(file_path):
    with open(file_path, 'r') as file:
        sys.stdin = file

        t = int(input().strip())

        for _ in range(t):
            try:
                n = int(input().strip())
            except ValueError:
                print(f"Incorrect input format in {file_path}.")
                return "Incorrect"

            # Read n more integers
            try:
                integers = list(map(int, input().split()))
            except ValueError:
                print(f"Incorrect input format in {file_path}.")
                return "Incorrect"
            
            if len(integers) != n:
                print(f"Expected {n} integers but got {len(integers)} in {file_path}.")
                return "Incorrect"

        # Check for extra input
        try:
            remaining_input = input()
            if remaining_input.strip():
                return "Incorrect"
        except EOFError:
            print(f"Input ended prematurely in {file_path}.")
            return "Incorrect"
        
        return "Correct"

def main(directory):
    input_files = [f for f in os.listdir(directory) if f.endswith('.in')]

    if not input_files:
        print(f"No .in files found in {directory}.")
        return

    for input_file in input_files:
        file_path = os.path.join(directory, input_file)

        # Redirect sys.stdin to the file
        with open(file_path, 'r') as f:
            result = process_file(file_path)

        # Reset sys.stdin to its original value
        sys.stdin = sys.__stdin__

        print(f"{input_file:20}: {result}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_test.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    main(directory)
