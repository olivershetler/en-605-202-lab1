"""This module contains tests for the converters module.
The test function names are self-explanatory, so additional
commentary is not provided.

The one thing to note is that the test functions only test the
conversion functions and not the helper functions. This is because
standard CI/CD practices dictate that we should only test the
public API of a module. The helper functions are not meant to be
used independently, so they are not tested.
"""

import pytest
from converters import *

def test_prefix_to_infix(prefix_infix_cases):
    for prefix, infix in prefix_infix_cases:
        assert prefix_to_infix(prefix) == infix

def test_prefix_to_infix_invalid(invalid_prefix_expressions):
    for expression in invalid_prefix_expressions:
        with pytest.raises(ValueError):
            prefix_to_infix(expression)

def test_prefix_to_postfix(prefix_postfix_cases):
    for prefix, postfix in prefix_postfix_cases:
        assert prefix_to_postfix(prefix) == postfix

def test_prefix_to_postfix_invalid(invalid_prefix_expressions):
    for expression in invalid_prefix_expressions:
        with pytest.raises(ValueError):
            prefix_to_postfix(expression)

def test_postfix_to_infix(postfix_infix_cases):
    for postfix, infix in postfix_infix_cases:
        assert postfix_to_infix(postfix) == infix

def test_postfix_to_infix_invalid(invalid_postfix_expressions):
    for expression in invalid_postfix_expressions:
        with pytest.raises(ValueError):
            postfix_to_infix(expression)

def test_postfix_to_prefix(postfix_prefix_cases):
    for postfix, prefix in postfix_prefix_cases:
        assert postfix_to_prefix(postfix) == prefix

def test_postfix_to_prefix_invalid(invalid_postfix_expressions):
    for expression in invalid_postfix_expressions:
        with pytest.raises(ValueError):
            postfix_to_prefix(expression)

def test_infix_to_prefix(infix_prefix_cases):
    for infix, prefix in infix_prefix_cases:
        assert infix_to_prefix(infix) == prefix

def test_infix_to_prefix_invalid(invalid_infix_expressions):
    for expression in invalid_infix_expressions:
        with pytest.raises(ValueError):
            infix_to_prefix(expression)

def test_infix_to_postfix(infix_postfix_cases):
    for infix, postfix in infix_postfix_cases:
        assert infix_to_postfix(infix) == postfix

def test_infix_to_postfix_invalid(invalid_infix_expressions):
    for expression in invalid_infix_expressions:
        with pytest.raises(ValueError):
            infix_to_postfix(expression)