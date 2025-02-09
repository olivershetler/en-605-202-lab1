import pytest

# a 3-tuple with infix, prefix, and postfix expressions that are equivalent to each other for testing
EXAMPLE_DATA_TUPLES = [
    ("(A + B)", "+AB", "AB+"),
    ("(A + (B * C))", "+A*BC", "ABC*+"),
    ("(A + ((B * C) - D))", "-+A*BCD", "ABC*D-+"),
    ("(A + ((B * C) - (D / E)))", "-+A*BC/DE", "ABC*DE/-+"),
    ("((A + (B * C)) - (D / (E ^ F)))", "-+A*BC/^DEF", "ABC*DEF^/-+"),
    ("A + B * C - D / E ^ F + G", "+-+A*BC/^DEF+G", "ABC*DEF^/-+G+"),
    ("A + B * C - D / E ^ F + G * H", "+-+A*BC/^DEF+*GH", "ABC*DEF^/-+G*H+"),
    ("A + B * C - D / E ^ F + G * H / I", "+-+A*BC/^DEF+*GH/I", "ABC*DEF^/-+G*H/I+"),
    ("A + B * C - D / E ^ F + G * H / I ^ J", "+-+A*BC/^DEF+*GH/IJ", "ABC*DEF^/-+G*H/IJ^/+")
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
    return ["A +", "A & B", "A^^B", "A + B +", "A + B C"]

@pytest.fixture
def invalid_prefix_expressions():
    """Simple test cases for invalid prefix expressions."""
    return ["A +", "& A B", "^ ^ A B C", "+ A B C"]

@pytest.fixture
def invalid_postfix_expressions():
    """Simple test cases for invalid postfix expressions."""
    return ["+ A", "A B &", "A B C ^ ^", "A B C +"]