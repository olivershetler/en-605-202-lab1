"""This module contains all the necessary tools for converting between infix, prefix, and postfix expressions.

For prefix and postfix to infix conversions, we follow the standard approach of using a stack to build the expression.

We use the Shunting-Yard algorithm for infix to postfix conversion and then reverse the result for infix to prefix conversion (since the algorithm is easier to implement for postfix).
"""

import re
import functools

# Set of valid operators for expression handling
OPERATORS = {'+', '-', '*', '/', '^'}
# Operator precedence mapping (higher value = higher precedence)
PRECEDENCE = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}
# Operator associativity rules
ASSOCIATIVITY = {'^': 'right', '+': 'left', '-': 'left', '*': 'left', '/': 'left'}

# Helper functions

def is_operator(token):
    """Return True if token is one of the allowed operators."""
    return token in OPERATORS

def is_operand(token):
    """Return True if token is a capital letter only."""
    return token.isalpha() and token.isupper()

def strip_whitespace(expression):
    """Remove all whitespace from the expression."""
    return "".join(expression.split())

def tokenize(expression):
    """
    Tokenize the expression with proper handling of operators and operands.
    """
    # First standardize the expression
    expr = standardize_expression(expression)
    
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i] in OPERATORS:
            # Handle double minus
            if expr[i] == '-' and i + 1 < len(expr) and expr[i + 1] == '-':
                tokens.append('+')
                i += 2
            else:
                tokens.append(expr[i])
                i += 1
        elif expr[i].isalpha():
            tokens.append(expr[i])
            i += 1
        elif expr[i] in '()':
            tokens.append(expr[i])
            i += 1
        else:
            i += 1  # Skip other characters
            
    return tokens


# Stack class for use in conversion functions

class Stack:
    """A simple stack class that wraps around the list class.
    Note to the TA: the professor said we could use a list as a
    componant of our stack class, so I did. I hope that's okay."""
    def __init__(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)


# Decorator for Preprocessing and type checking

def preprocess(func):
    """
    A decorator that checks that the expression is a string
    and strips out all whitespace.
    """
    @functools.wraps(func)
    def wrapper(expression, *args, **kwargs):
        if not isinstance(expression, str):
            raise ValueError(f"Expression must be a string; got {type(expression)}")
        expression = strip_whitespace(expression)
        return func(expression, *args, **kwargs)
    return wrapper


# Validate the functions by printing True or False

def validate_infix(expression):
    """
    Fully validate an infix expression.

    Three level checks to debug the invalid expression inputs from initial testing.
      - The expression must consist only of letters, digits,
         the operators (+, -, *, /, ^), and round parentheses.
      - Balanced equations via '(' and a corresponding ')'.
      - Proper token order based on its kind the tokens (operands, operators, and parentheses) must
         be in a syntactically valid sequence. For example:
            - The expression cannot start with an operator.
            - Two operands cannot appear in a row.
            - An operator cannot immediately follow an opening parenthesis.
            - A closing parenthesis cannot appear when an operand is expected.

    Additionally, the expression must contain at least one operator.

    Returns:
      True if the expression is valid; otherwise, False.
    """
    # Step 1: Check allowed characters.
    allowed_pattern = re.compile(r'^[A-Za-z0-9+\-*/^()]+$')
    if not allowed_pattern.fullmatch(expression):
        return False

    # Tokenize the expression.
    tokens = list(expression)
    if not tokens:
        return False

    # Step 2: Check balanced parentheses and token order.
    paren_stack = []
    # When True we expect an operand or an open parenthesis.
    # When False we expect an operator or a closing parenthesis.
    expecting_operand = True

    for token in tokens:
        if token == '(':
            paren_stack.append(token)
            expecting_operand = True
        elif token == ')':
            if expecting_operand:
                return False
            if not paren_stack:
                return False
            paren_stack.pop()
            # A closed parenthesis represents a complete operand.
            expecting_operand = False
        elif is_operand(token):
            if not expecting_operand:
                return False
            expecting_operand = False
        elif is_operator(token):
            if expecting_operand:
                return False
            expecting_operand = True
        else:
            # Should not happen because of the allowed pattern.
            return False

    # Final checks: we must not be expecting an operand and all parentheses must be closed.
    if expecting_operand or paren_stack:
        return False

    # Additional check: there must be at least one operator.
    if not any(is_operator(token) for token in tokens):
        return False

    return True


def validate_prefix(expression):
    """
    Validate a prefix expression by counting operators and operands.
    For a valid prefix expression, at each point reading from left to right,
    the number of operators must be greater than operands until the end.
    """
    tokens = tokenize(expression)
    if not tokens:
        return False
        
    # First token must be an operator
    if not is_operator(tokens[0]):
        return False
        
    operator_count = 0
    operand_count = 0
    
    for token in tokens:
        if is_operator(token):
            operator_count += 1
        elif is_operand(token):
            operand_count += 1
        else:
            return False
            
        # At any point, if we have more operands than needed, it's invalid
        if operand_count > operator_count + 1:
            return False
            
    # At the end, operands should be exactly one more than operators
    return operand_count == operator_count + 1


def validate_postfix(expression):
    """
    Validate a postfix expression by mirroring.
    """
    tokens = tokenize(expression)
    # Must have at least one operator.
    if not any(is_operator(token) for token in tokens):
        return False

    stack = Stack()
    for token in tokens:
        if is_operand(token):
            stack.push(token)
        elif is_operator(token):
            # Need at least two operands for an operator
            if len(stack) < 2:
                return False
            # Pop two operands and push result placeholder
            stack.pop()
            stack.pop()
            stack.push('X')
        elif token in [' ', '\t', '\n']:
            continue
        else:
            return False
            
    # At the end, should have exactly one result
    return len(stack) == 1



# Conversion Functions

@preprocess
def prefix_to_infix(expression):
    """
    Convert a prefix expression to infix.
    This algorithm assumes single-character tokens.
    """
    if not validate_prefix(expression):
        raise ValueError("Invalid prefix expression.")
    tokens = tokenize(expression)
    stack = Stack()
    for token in reversed(tokens):
        if is_operator(token):
            try:
                op1 = stack.pop()
                op2 = stack.pop()
            except IndexError:
                raise ValueError("Invalid prefix expression.")
            # Parenthesize the resulting expression.
            stack.push(f"({op1} {token} {op2})")
        elif is_operand(token):
            stack.push(token)
        elif token == ' ':
            continue
        else:
            raise ValueError(f"Unexpected token: {token}")
    if len(stack) != 1:
        raise ValueError("Invalid prefix expression.")
    return stack.pop()

@preprocess
def postfix_to_infix(expression):
    """
    Convert a postfix expression to infix.
    This algorithm assumes single-character tokens.
    """
    if not validate_postfix(expression):
        raise ValueError("Invalid postfix expression.")
    tokens = tokenize(expression)
    stack = Stack()
    for token in tokens:
        if is_operand(token):
            stack.push(token)
        elif is_operator(token):
            try:
                op2 = stack.pop()
                op1 = stack.pop()
            except IndexError:
                raise ValueError("Invalid postfix expression.")
            stack.push(f"({op1} {token} {op2})")
        elif token == ' ':
            continue
        else:
            raise ValueError(f"Unexpected token: {token}")
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression.")
    return stack.pop()


def _shunting_yard(tokens):
    """
    Convert a token list from infix to postfix using the shunting-yard algorithm.
    Returns a list of tokens in postfix order.
    """
    output = []
    op_stack = Stack()
    for token in tokens:
        if is_operand(token):
            output.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            if op_stack.is_empty():
                raise ValueError("Mismatched parentheses.")
            op_stack.pop()  # Discard the '('
        elif is_operator(token):
            while (not op_stack.is_empty() and op_stack.peek() != '(' and
                   ((ASSOCIATIVITY[token] == 'left' and PRECEDENCE[token] <= PRECEDENCE[op_stack.peek()]) or
                    (ASSOCIATIVITY[token] == 'right' and PRECEDENCE[token] < PRECEDENCE[op_stack.peek()]))):
                output.append(op_stack.pop())
            op_stack.push(token)
        else:
            raise ValueError(f"Unexpected token: {token}")
    while not op_stack.is_empty():
        top = op_stack.pop()
        if top == '(':
            raise ValueError("Mismatched parentheses.")
        output.append(top)
    return output

@preprocess
def infix_to_postfix(expression):
    """
    Convert an infix expression to postfix (Reverse Polish Notation).
    Uses the shunting-yard algorithm.
    """
    if not validate_infix(expression):
        raise ValueError("Invalid infix expression.")
    tokens = tokenize(expression)
    postfix_tokens = _shunting_yard(tokens)
    # Return as a string without spaces (or join with spaces if desired)
    result = "".join(postfix_tokens)
    if not validate_postfix(result):
        raise ValueError("Conversion resulted in an invalid postfix expression.")
    return result

@preprocess
def infix_to_prefix(expression):
    """
    Convert an infix expression to prefix (Polish Notation).
    The algorithm is:
      1. Reverse the infix string.
      2. Replace '(' with ')' and vice-versa.
      3. Convert to postfix (using the shunting-yard algorithm).
      4. Reverse the result.
    """
    if not validate_infix(expression):
        raise ValueError("Invalid infix expression.")
    # Reverse tokens and swap parentheses.
    tokens = tokenize(expression)
    tokens = tokens[::-1]
    swapped = []
    for token in tokens:
        if token == '(':
            swapped.append(')')
        elif token == ')':
            swapped.append('(')
        else:
            swapped.append(token)
    # Convert to postfix using the shunting-yard algorithm.
    postfix = _shunting_yard(swapped)
    # The prefix is the reverse of the postfix.
    prefix_tokens = postfix[::-1]
    result = "".join(prefix_tokens)
    if not validate_prefix(result):
        raise ValueError("Conversion resulted in an invalid prefix expression.")
    return result

def prefix_to_postfix(expression):
    """Convert prefix to postfix via infix as an intermediate representation."""
    infix = prefix_to_infix(expression)
    return infix_to_postfix(infix)

def postfix_to_prefix(expression):
    """Convert postfix to prefix via infix as an intermediate representation."""
    infix = postfix_to_infix(expression)
    return infix_to_prefix(infix)

def clean_expression(expression: str) -> str:
    """
    Clean the expression by:
    1. Replacing en-dash with regular hyphen
    2. Ensuring consistent spacing
    3. Removing any invalid characters
    
    Args:
        expression (str): The input expression to clean
    Returns:
        str: The cleaned expression
    """
    # Replace en-dash with regular hyphen
    expression = expression.replace('–', '-')
    
    # Remove any quotes or invalid characters
    expression = ''.join(c for c in expression if c.isalnum() or c in '+-*/^ ' or c in '()')
    
    # Ensure consistent spacing
    return ' '.join(expression.split())

def validate_expression(expression: str, expr_type: str) -> bool:
    """
    Basic validation of expression format
    
    Args:
        expression (str): The expression to validate
        expr_type (str): Type of expression ('infix', 'prefix', or 'postfix')
    Returns:
        bool: True if expression appears valid
    """
    tokens = expression.split()
    
    # Basic check - need at least one operator and one operand
    if not any(t in '+-*/^' for t in expression):
        return False
    if not any(t.isalnum() for t in tokens):
        return False
        
    return True

def standardize_expression(expr):
    """Standardize the expression format"""
    # Replace en-dash and em-dash with regular minus
    expr = expr.replace('–', '-').replace('—', '-')
    
    # Remove all spaces and quotes
    expr = ''.join(expr.split())
    expr = expr.replace('"', '')
    
    # Handle any other special characters
    expr = ''.join(c for c in expr if c.isalnum() or c in '+-*/^()' or c == '-')
    
    return expr
