import os
import resource
import sys
import subprocess
import time
import argparse
import re
import tempfile

SOURCE_EXTENSIONS = {'.c', '.cc', '.cpp', '.cxx'}


def set_stack_limit():
    stack_size = 256 * 1024 * 1024  
    resource.setrlimit(resource.RLIMIT_STACK, (stack_size, stack_size))


def find_all_test_cases(tests_folder):
    """Recursively find all .in files and their corresponding .out files."""
    test_cases = []
    
    for root, dirs, files in os.walk(tests_folder):
        for file in files:
            if file.endswith('.in'):
                input_path = os.path.join(root, file)
                output_path = input_path.replace('.in', '.out')
                
                # Only add the pair if the .out file exists
                if os.path.exists(output_path):
                    # Store relative paths for cleaner display
                    rel_input = os.path.relpath(input_path, tests_folder)
                    test_cases.append((input_path, output_path, rel_input))
    
    def natural_key(item):
        return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', item[2])]

    return sorted(test_cases, key=natural_key)


def find_solution_files(path):
    if os.path.isfile(path):
        return [path]

    solution_files = []
    for root, dirs, files in os.walk(path):
        dirs.sort()
        for file in sorted(files):
            if os.path.splitext(file)[1] in SOURCE_EXTENSIONS:
                solution_files.append(os.path.join(root, file))

    return solution_files


def check_outputs(code_file, tests_folder, compiler='gcc', flags=['-O2'], time_limit=None):
    print(f"Checking solution: {code_file}")
    print(f"Using test cases from folder: {tests_folder}\n")
    if time_limit is not None:
        print(f"Time limit per test: {time_limit:.3f}s\n")

    verdict = "AC"
    max_execution_time = 0
    AC_count = 0
    
    # Find all test cases recursively
    test_cases = find_all_test_cases(tests_folder)
    
    if not test_cases:
        print(f"Error: No test cases found in {tests_folder}")
        return
    
    fd, executable_path = tempfile.mkstemp(prefix='sec_cq3_solution_')
    os.close(fd)
    compile_command = [compiler, code_file] + flags + ['-o', executable_path]
    process = subprocess.Popen(compile_command, stderr=subprocess.PIPE)
    _, compile_error = process.communicate()

    if process.returncode != 0:
        print(f"Compilation error for {code_file}:")
        print(compile_error.decode())
        try:
            os.remove(executable_path)
        except:
            pass
        return

    for index, (input_path, output_path, rel_input) in enumerate(test_cases, 1):
        try:
            with open(output_path, 'r') as f:
                expected_output = f.read().strip()
                
            with open(input_path, 'r') as in_f:
                start_time = time.time()
                process = subprocess.Popen(
                    [executable_path],
                    stdin=in_f,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=set_stack_limit
                )

                try:
                    actual_output, stderr = process.communicate(timeout=time_limit)
                except subprocess.TimeoutExpired:
                    process.kill()
                    actual_output, stderr = process.communicate()
                    end_time = time.time()
                    print(f"{index:2}: {rel_input:40}: TLE, time: {end_time - start_time:.3f}")
                    verdict = "WA"
                    continue

                end_time = time.time()

            if process.returncode != 0:
                print(f"{index:2}: {rel_input:40}: Error - {stderr.decode()}")
                verdict = "WA"
                continue

            if actual_output.decode().strip() != expected_output:
                print(f"{index:2}: {rel_input:40}: WA")
                verdict = "WA"
                continue

            execution_time = end_time - start_time
            AC_count += 1
            print(f"{index:2}: {rel_input:40}: AC, time: {execution_time:.3f}")
            max_execution_time = max(max_execution_time, execution_time)
        
        except Exception as e:
            print(f"{index:2}: {rel_input:40}: Error - {str(e)}")
            verdict = "Error"
    
    # Clean up the compiled solution
    try:
        os.remove(executable_path)
    except:
        pass

    total_cases = len(test_cases)
    print(f"\nVERDICT: {verdict}")
    print(f"Total test cases: {total_cases}")
    print(f"AC count: {AC_count}/{total_cases}")
    print(f"WA count: {total_cases - AC_count}/{total_cases}")
    print(f"Max execution time: {max_execution_time:.3f}")
    print("-"*50)


def main():
    parser = argparse.ArgumentParser(description='Code Checker')
    parser.add_argument(
        'code_path', help='Path to a code file or a folder containing solution files')
    parser.add_argument(
        'tests_folder', help='Path to the folder containing test cases (e.g., ./tests)')
    parser.add_argument('compiler', nargs='?', default='g++',
                        help='Compiler to use (e.g., gcc)')
    parser.add_argument(
        '--flags', nargs='+', default=['-std=c++20'], help='Compiler flags as a list (e.g., --flags -O2 -Wall)')
    parser.add_argument(
        '--tl', type=float, default=None, help='Per-test time limit in seconds. Runs exceeding this are killed and marked TLE.')

    args = parser.parse_args()

    code_path = args.code_path
    tests_folder = args.tests_folder
    compiler = args.compiler
    flags = args.flags

    # Verify whether code_path, tests_folder, and compiler exist
    if not os.path.exists(code_path):
        print(f"Error: The code path '{code_path}' does not exist.")
        return

    if not os.path.exists(tests_folder):
        print(f"Error: The tests folder '{tests_folder}' does not exist.")
        return

    if args.tl is not None and args.tl <= 0:
        print("Error: --tl must be positive.")
        return

    solution_files = find_solution_files(code_path)
    if not solution_files:
        print(f"Error: No solution files with extensions {sorted(SOURCE_EXTENSIONS)} found in '{code_path}'.")
        return

    for code_file in solution_files:
        check_outputs(code_file, tests_folder, compiler, flags, args.tl)


if __name__ == "__main__":
    main()
