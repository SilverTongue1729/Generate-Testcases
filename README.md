# Generate-Testcases

A repository to quickly generate and validate test cases for DSA-style programming problems.

## Overview

This repository provides Python scripts and a Jupyter Notebook to streamline the process of:

- **Generating** test case inputs (including medium and large test cases)
- **Validating** input formats
- **Creating** test files (`.in`, `.out` pairs) from a combined input file
- **Checking** solution outputs against these test cases

## Usage

**Assumptions:**

- Output is unique for each testcase (Will need to modify [checker.py](tools/checker.py) if not).

**Input:**

- Each individual testcase in `inputs/*.txt` must be separated by an empty line.
- Fill [samples.txt](inputs/samples.txt) with sample test cases from the problem statement.
- Fill [small.txt](inputs/small.txt) with handcrafted test cases if needed.
- Modify [generator_medium.py](generators/generator_medium.py) and [generator_large.py](generators/generator_large.py) to generate medium and large inputs respectively.
- Modify [validator.py](tools/validator.py) to validate the input format.
- Using an AI model such as ChatGPT to write the generators and validator can significantly accelerate the process.

**Generating Testcases:**

- Follow instructions and run cells in [generate_testcases.ipynb](generate_testcases.ipynb)
- Alternatively run the following commands from the root directory:

```bash
# clear input files
truncate -s 0 *.txt inputs/*.txt
# generate medium inputs
python generators/generator_medium.py inputs/medium.txt
# generate large inputs
python generators/generator_large.py inputs/large.txt
# concate all inputs into input_all.txt
cat inputs/samples.txt <(echo -e "\n\n") inputs/small.txt <(echo -e "\n\n") inputs/medium.txt <(echo -e "\n\n") inputs/large.txt > inputs/all_inputs.txt

# generate tests
python tools/testcase_generator.py solutions/correct_solution_01.c inputs/all_inputs.txt tests/ 1
# how to use checker.py
python tools/checker.py -h
# check solution
python tools/checker.py solutions/correct_solution_01.c tests/
# validate tests
python scripts/check_test.py tests/
# zip tests
zip -r tests.zip tests/
```

**Solutions**:

- Write both correct and wrong solutions in [solutions/](solutions/).
- If the problem allows for partial marks with multiple batches of test, ensure to write a solution that gets partial marks, and that edges cases are covered in both batches of testcases.

## Repository Structure

```bash
.
├── LICENSE
├── README.md
├── generate_testcases.ipynb   # Commands to generate testcases
├── inputs/
│   ├── samples.txt         # Problem sample testcases
│   ├── small.txt           # Handcrafted small testcases
│   ├── medium.txt          # Medium testcases (generated)
│   ├── large.txt           # Large testcases (generated)
│   └── all_inputs.txt      # Combined input file
├── generators/
│   ├── generator_medium.py        # Generates medium testcases
│   └── generator_large.py         # Generates large testcases
├── tools/
│   ├── testcase_generator.py      # Creates .in/.out files from combined inputs
│   ├── checker.py                 # Validates solution outputs
│   └── validator.py               # Validates test input format
├── solutions/
│   ├── correct_solution_01.c      # Sample correct solution
│   └── wrong_solution_01.c        # Sample wrong solution
└── tests/                         # Auto-generated test files
```
