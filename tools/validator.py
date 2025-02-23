import os
import sys
from collections import deque

def process_in_file(file_path):
    """
    Process and verify the format of the input file.
    
    Expected Input Format:
      - First line: single integer n (1 ≤ n ≤ 10^6), the number of nodes.
      - Second line: n space-separated integers (each 0 or 1) representing the passenger array.
      - Third line: n space-separated integers representing the parent array.
          * For each node i, the value is its parent's index.
          * Exactly one node must have parent -1 (the root).
          * For every other node, the parent must be between 1 and n (and not 0).
      - No extra non-empty lines should be present.
    
    Additionally, verifies that the parent array forms a connected tree (no cycles, exactly one tree).
    """
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip() != ""]
    except Exception as e:
        return f"Error reading file: {e}"

    if len(lines) != 3:
        return f"Expected 3 non-empty lines (n, passenger array, parent array) but got {len(lines)}."

    # Process first line: number of nodes
    try:
        n = int(lines[0])
    except ValueError:
        return "First line must be an integer representing n."
    if not (1 <= n <= 10**6):
        return f"n must be between 1 and 10^6, got {n}."

    # Process second line: passenger array
    passenger_tokens = lines[1].split()
    if len(passenger_tokens) != n:
        return f"Passenger array: Expected {n} integers but got {len(passenger_tokens)}."
    try:
        passengers = [int(token) for token in passenger_tokens]
    except ValueError:
        return "Passenger array must contain integers."
    for p in passengers:
        if p not in (0, 1):
            return f"Passenger array values must be 0 or 1, found {p}."

    # Process third line: parent array
    parent_tokens = lines[2].split()
    if len(parent_tokens) != n:
        return f"Parent array: Expected {n} integers but got {len(parent_tokens)}."
    try:
        parents = [int(token) for token in parent_tokens]
    except ValueError:
        return "Parent array must contain integers."

    # Validate parent array:
    # - Exactly one root (value -1) should exist.
    # - For non-root nodes, the parent must be in the range [1, n]
    root_count = 0
    for idx, p in enumerate(parents, start=1):
        if p == -1:
            root_count += 1
        else:
            if not (1 <= p <= n):
                return f"Invalid parent value {p} for node {idx}. Must be -1 or between 1 and {n}."
    if root_count != 1:
        return f"Expected exactly one root (parent = -1), but found {root_count}."

    # Check that the parent array forms a connected tree.
    # Build adjacency list (child pointers) for each node.
    children = {i: [] for i in range(1, n+1)}
    root = None
    for i, p in enumerate(parents, start=1):
        if p == -1:
            root = i
        else:
            children[p].append(i)

    # Use BFS/DFS to count reachable nodes from the root.
    visited = set()
    queue = deque([root])
    while queue:
        curr = queue.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        for child in children[curr]:
            queue.append(child)

    if len(visited) != n:
        return f"The tree is not connected. Only {len(visited)} out of {n} nodes are reachable from the root."

    return "Correct"

def process_out_file(file_path):
    """
    Process and verify the format of the output file.
    
    Expected Output Format:
      - A single line with a single integer (which can be 0 or positive).
      - No extra non-empty lines.
    """
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip() != ""]
    except Exception as e:
        return f"Error reading file: {e}"

    if len(lines) != 1:
        return f"Expected exactly 1 non-empty line in output file but found {len(lines)}."
    try:
        result = int(lines[0])
        if result < 0:
            return "Output must be a non-negative integer."
    except ValueError:
        return "Output file must contain a single integer."
    
    return "Correct"

def main(directory):
    input_files = [f for f in os.listdir(directory) if f.endswith('.in')]
    output_files = [f for f in os.listdir(directory) if f.endswith('.out')]

    if not input_files:
        print(f"No .in files found in {directory}.")
        return
    if not output_files:
        print(f"No .out files found in {directory}.")
        return

    print("Input file verification:")
    for input_file in sorted(input_files):
        file_path = os.path.join(directory, input_file)
        result = process_in_file(file_path)
        print(f"{input_file:20}: {result}")

    print("\nOutput file verification:")
    for output_file in sorted(output_files):
        file_path = os.path.join(directory, output_file)
        result = process_out_file(file_path)
        print(f"{output_file:20}: {result}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_test.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    main(directory)
