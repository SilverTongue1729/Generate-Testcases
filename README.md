# Create testcases fast

## Description

- `inputs/` contains input files and the relevant python code.

  - `inputs/make_inputs_medium.py` and `inputs/make_inputs_large.py` are used to generate inputs.
  - The `.txt` files contain inputs which each testcase separated by a newline.
- `tests/` contains testcases with `.in` and `.out` files.
- `sols/` contains solution files.
- `scripts/` contains scripts, only `check_test.py` needs to be modified to validate tests.

## Usage

- write the relevant python code in `inputs/make_medium_inputs.py` and `inputs/make_large_inputs.py` to generate inputs.
- write the relevant python code in `check_test.py` to validate input.
- open `script.ipynb`, run the cells

## Files

``python make_tests.py sol.c input.txt tests/ first_testcase_number``

- I assume that each testcase in input.txt is separated by a newline
- multiple empty lines in input.txt will be ignored

``python check_sol.py sol.c tests/``

- `check_sol.py` will compile `sol.c` and run it against each testcase in tests/

``python check_test.py tests/``

- `check_test.py` will verify if the inputs are in the correct format

``python inputs/make_medium_inputs.py inputs/medium_input.txt````python inputs/make_large_inputs.py inputs/large_input.txt``

- Use for generating inputs
- Write your own python code depending on the problem

## Example

- this folder contains a sample sol.c and input.txt
