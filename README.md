# README

This readme file details how to install and run the program as well as how to run the tests.

## Problem Statement

This lab is about methods for converting between different representations of arithmetic expressions. The three representations we will consider are: infix, postfix, and prefix. Infix is the usual way of writing arithmetic expressions, with the operator between the operands. Postfix is a way of writing arithmetic expressions where the operator follows the operands. Prefix is a way of writing arithmetic expressions where the operator precedes the operands. For example, the infix expression `3 + 4` is equivalent to the postfix expression `3 4 +` and the prefix expression `+ 3 4`.

## Repository Organization

The source code is in the `lab1` directory. The `lab1` diretory contains the following modules:
1. `converters.py`: Contains functions to convert among infix, postfix, and prefix expressions as well as helper functions for use within the conversion functions. Helpers include functions to check the precedence of operators, to check if a character is an operator, and to validate the input expressions.
2. `main.py`: Contains the main function to produce output for the provided data.

The `tests` directory contains the test cases for the functions in the `converters.py` module implemented with `pytest`. The `conftest.py` file contains the fixtures used in the test cases including the test strings and expected results. The `test_converters.py` file contains the test cases for the functions in the `converters.py` module.

The `resources` directory contains a `config.yml` file, which contains the configuration for the input and output file paths as well as `data` and `output` directories that contain the input and output files, respectively.

Input and output files are .txt formatted as per the assignment guidelines.

At the base of the repository, there is a `pyproject.toml` file that contains the project metadata and dependencies.

## Dependencies

To install the program and its dependencies, cd into the repoistory and execute the following command in the terminal:

```bash
pip install -e .
```

The package was tested using a virtual environment with python 3.12.4. Consider creating a virtual environment to run the program using the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## How to Run

To run the program, execute the following command in the terminal:

```bash
python src/main.py
```

The program will read the input file, process the data, and write the output to the output file.

## How to Test

To run the tests, execute the following command in the terminal:

```bash
pytest -s
```

The `-s` flag is used to display the output of the tests.