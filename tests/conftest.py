"""This module contains fixtures for testing the converters.
"""

import pytest

# a 3-tuple with infix, prefix, and postfix expressions that are equivalent to each other for testing
EXAMPLE_DATA_TUPLES = [
    # 1. Simple addition.
    ("(A + B)", "+AB", "AB+"),

    # 2. Mixed addition and multiplication.
    ("(A + (B * C))", "+A*BC", "ABC*+"),

    # 3. Exponentiation (right–associative).
    ("(A ^ (B ^ C))", "^A^BC", "ABC^^"),

    # 4. Grouped addition/subtraction with multiplication.
    ("((A + B) * (C - D))", "*+AB-CD", "AB+CD-*"),

    # 5. Combined operations with nested grouping.
    ("((A + (B * C)) - (D / E))", "-+A*BC/DE", "ABC*+DE/-"),
]

GENERALLY_INVALID_EXPRESSIONS = [
    # 1. Empty expression.
    "",

    # 2. Single operand.
    "A",

    # 3. Single operator.
    "+",

    # 4. Single operator and operand.
    "A +",

    # 5. Single operator and operand.
    "A + B C",

    # 6. Wrong type (numeric)
    123,

    # 7. Wrong type (list of strings).
    ["A", "+", "B"],

    # 8. Contains invalid characters.
    "A & B",

    # 9. Contains invalid characters.
    "X @ Y",
]

INVALID_INFIX_EXPRESSIONS = GENERALLY_INVALID_EXPRESSIONS + [
    # 1. Imbalanced parentheses.
    "(A + B",
    "A + B)",
    # 2. invalid operand order
    "A + B +",
]

INVALID_PREFIX_EXPRESSIONS = GENERALLY_INVALID_EXPRESSIONS + [
    # 1. Too few operands.
    "+ A",
    # 2. Too many operands.
    "+ A B C",
    # 3. invalid operand order
    "+ A B +",
]

INVALID_POSTFIX_EXPRESSIONS = GENERALLY_INVALID_EXPRESSIONS + [
    # 1. Too few operands.
    "A +",
    # 2. Too many operands.
    "A B C +",
    # 3. invalid operand order
    "A + B + C",
]

@pytest.fixture
def infix_postfix_cases():
    """Simple test cases for infix to postfix conversion.
    The first element of the tuple is the infix expression
    and the second element is the expected postfix expression.
    """
    return [(ex[0], ex[2]) for ex in EXAMPLE_DATA_TUPLES]

@pytest.fixture
def infix_prefix_cases():
    """Simple test cases for infix to prefix conversion.
    The first element of the tuple is the infix expression
    and the second element is the expected prefix expression.
    """
    return [(ex[0], ex[1]) for ex in EXAMPLE_DATA_TUPLES]

@pytest.fixture
def prefix_infix_cases():
    """Simple test cases for prefix to infix conversion.
    The first element of the tuple is the prefix expression
    and the second element is the expected infix expression.
    """
    return [(ex[1], ex[0]) for ex in EXAMPLE_DATA_TUPLES]

@pytest.fixture
def postfix_infix_cases():
    """Simple test cases for postfix to infix conversion.
    The first element of the tuple is the postfix expression
    and the second element is the expected infix expression.
    """
    return [(ex[2], ex[0]) for ex in EXAMPLE_DATA_TUPLES]

@pytest.fixture
def postfix_prefix_cases():
    """Simple test cases for postfix to prefix conversion.
    The first element of the tuple is the postfix expression
    and the second element is the expected prefix expression.
    """
    return [(ex[2], ex[1]) for ex in EXAMPLE_DATA_TUPLES]

@pytest.fixture
def prefix_postfix_cases():
    """Simple test cases for prefix to postfix conversion.
    The first element of the tuple is the prefix expression
    and the second element is the expected postfix expression.
    """
    return [(ex[1], ex[2]) for ex in EXAMPLE_DATA_TUPLES]

@pytest.fixture
def invalid_infix_expressions():
    """Simple test cases for invalid infix expressions."""
    return INVALID_INFIX_EXPRESSIONS

@pytest.fixture
def invalid_prefix_expressions():
    """Simple test cases for invalid prefix expressions."""
    return INVALID_PREFIX_EXPRESSIONS

@pytest.fixture
def invalid_postfix_expressions():
    """Simple test cases for invalid postfix expressions."""
    return INVALID_POSTFIX_EXPRESSIONS