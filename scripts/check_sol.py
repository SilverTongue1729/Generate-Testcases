import os
import sys
import subprocess
import time
import argparse


def check_outputs(code_file, tests_folder, compiler='gcc', flags=['-O2']):
    print(f"Checking solution: {code_file}")
    print(f"Using test cases from folder: {tests_folder}\n")

    verdict = "AC"
    max_execution_time = 0
    index = 1  # Initialize the index to 1
    AC_count = 0

    for input_file in sorted(os.listdir(tests_folder)):
        if input_file.endswith('.in'):
            input_path = os.path.join(tests_folder, input_file)
            output_path = os.path.join(
                tests_folder, input_file.replace('.in', '.out'))
            expected_output = open(output_path, 'r').read().strip()

            compile_command = [compiler, code_file] + \
                flags + ['-o', 'solution']
            process = subprocess.Popen(compile_command, stderr=subprocess.PIPE)
            _, compile_error = process.communicate()

            if process.returncode != 0:
                print(f"Compilation error for {code_file}:")
                print(compile_error.decode())
                return

            start_time = time.time()
            process = subprocess.Popen(
                ['./solution'], stdin=open(input_path, 'r'), stdout=subprocess.PIPE)
            actual_output, stderr = process.communicate()
            end_time = time.time()

            os.remove('solution')

            if process.returncode != 0:
                print(f"{index:2:}: {input_file:20}: Error - {stderr.decode()}")
                verdict = "WA"
                continue

            if actual_output.decode().strip() != expected_output:
                print(f"{index:2}: {input_file:20}: WA")
                verdict = "WA"
                continue

            execution_time = end_time - start_time
            AC_count += 1
            print(f"{index:2}: {input_file:20}: AC, time: {execution_time:.3f}")
            max_execution_time = max(max_execution_time, execution_time)

            index += 1  # Increment the index

    print(f"\nVERDICT: {verdict}")
    print(f"Total test cases: {index - 1}")
    print(f"AC count: {AC_count}/{index - 1}")
    print(f"WA count: {index - 1 - AC_count}/{index - 1}")
    print(f"Max execution time: {max_execution_time:.3f}")
    print("-"*50)


def main():
    parser = argparse.ArgumentParser(description='Code Checker')
    parser.add_argument(
        'code_file', help='Path to the code file (e.g., sol.c)')
    parser.add_argument(
        'tests_folder', help='Path to the folder containing test cases (e.g., ./tests)')
    parser.add_argument('compiler', nargs='?', default='gcc',
                        help='Compiler to use (e.g., gcc)')
    # parser.add_argument('--flags', nargs='*', default=[
    #                     '-O2'], help='Compiler flags as a list enclosed in double quotes (e.g., "--flags -O2 -Wall")')
    parser.add_argument(
        '--flags', nargs='+', default=['-O2'], help='Compiler flags as a list (e.g., --flags -O2 -Wall)')

    args = parser.parse_args()

    code_file = args.code_file
    tests_folder = args.tests_folder
    compiler = args.compiler
    flags = args.flags

    # Verify whether code_file, tests_folder, and compiler exist
    if not os.path.exists(code_file):
        print(f"Error: The code file '{code_file}' does not exist.")
        return

    if not os.path.exists(tests_folder):
        print(f"Error: The tests folder '{tests_folder}' does not exist.")
        return

    check_outputs(code_file, tests_folder, compiler, flags)


if __name__ == "__main__":
    main()
