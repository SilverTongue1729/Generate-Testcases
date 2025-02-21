import os
import resource
import sys
import subprocess

def set_stack_limit():
    stack_size = 256 * 1024 * 1024  
    resource.setrlimit(resource.RLIMIT_STACK, (stack_size, stack_size))

def create_test_files(input_file, output_folder, start_number=1):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()

    test_cases = []
    current_test = []

    for line in lines:
        if line.strip():  # Non-empty line
            current_test.append(line)
        elif current_test:  # Empty line and there's a current test
            test_cases.append(current_test)
            current_test = []

    # Append the last test case if it's not empty
    if current_test:
        test_cases.append(current_test)

    for idx, test_case in enumerate(test_cases, start=start_number - 1):
        input_path = os.path.join(output_folder, f'{idx + 1}.in')
        output_path = os.path.join(output_folder, f'{idx + 1}.out')

        with open(input_path, 'w') as in_f:
            in_f.write('\n'.join(test_case))

        yield input_path, output_path


def compile_and_run(code_file, input_path, output_path):
    subprocess.run(['gcc', code_file, '-o', 'solution'])
    subprocess.run(
        ['./solution'],
        stdin=open(input_path, 'r'),
        stdout=open(output_path, 'w'),
        preexec_fn=set_stack_limit
    )
    os.remove('solution')


def main():
    if len(sys.argv) != 5:
        print("Usage: python script.py sol.c input.txt ./tests start_number")
        return

    code_file = sys.argv[1]
    input_file = sys.argv[2]
    output_folder = sys.argv[3]
    start_number = int(sys.argv[4])

    os.makedirs(output_folder, exist_ok=True)

    for input_path, output_path in create_test_files(input_file, output_folder, start_number):
        compile_and_run(code_file, input_path, output_path)
        print(f'Test case {input_path} completed.')


if __name__ == "__main__":
    main()
