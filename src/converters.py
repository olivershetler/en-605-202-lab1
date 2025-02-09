import re
import functools

# -- Constants and Helpers --

# Allowed operators and their precedence/associativity
OPERATORS = {'+', '-', '*', '/', '^'}
PRECEDENCE = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}
# Note: '^' is right-associative; all others are left-associative.
ASSOCIATIVITY = {'^': 'right', '+': 'left', '-': 'left', '*': 'left', '/': 'left'}

def is_operator(token):
    """Return True if token is one of the allowed operators."""
    return token in OPERATORS

def is_operand(token):
    """Return True if token is a digit or a letter."""
    return token.isdigit() or token.isalpha()

def strip_whitespace(expression):
    """Remove all whitespace from the expression."""
    return "".join(expression.split())

def tokenize(expression):
    """
    Tokenize the expression.
    If there are spaces, assume tokens are space–separated.
    Otherwise, return a list of single characters.
    """
    if " " in expression:
        return expression.split()
    return list(expression)


# Stack class for use in conversion functions

class Stack:
    """A simple stack wrapper."""
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


# -- Decorator for Preprocessing --

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


# -- Validation Functions --

def validate_infix(expression):
    """
    Check if the infix expression is valid.
    This basic validator accepts operands (letters/digits),
    allowed operators, and round parentheses.
    """
    # Allow letters, digits, operators, and parentheses
    pattern = re.compile(r'^[A-Za-z0-9\+\-\*\/\^\(\)]*$')
    if not pattern.fullmatch(expression):
        return False

    # Check balanced parentheses
    stack = Stack()
    for char in expression:
        if char == '(':
            stack.push(char)
        elif char == ')':
            if stack.is_empty():
                return False
            stack.pop()
    if not stack.is_empty():
        return False

    # (Further validation on token order is possible but omitted.)
    return True

def validate_prefix(expression):
    """
    Validate a prefix expression.
    We assume that a prefix expression (with single–character tokens)
    is valid if, when scanned from right to left,
    every operator finds at least two operands.
    Tokens are assumed to be contiguous (no spaces needed).
    """
    tokens = tokenize(expression)
    stack = Stack()
    # Process tokens in reverse order.
    for token in reversed(tokens):
        if is_operand(token):
            stack.push(token)
        elif is_operator(token):
            if len(stack) < 2:
                return False
            # Pop two operands and push a dummy operand.
            stack.pop()
            stack.pop()
            stack.push('X')
        else:
            return False
    return len(stack) == 1

def validate_postfix(expression):
    """
    Validate a postfix expression.
    We assume that a postfix expression (with single–character tokens)
    is valid if every operator finds at least two operands when scanning left to right.
    """
    tokens = tokenize(expression)
    stack = Stack()
    for token in tokens:
        if is_operand(token):
            stack.push(token)
        elif is_operator(token):
            if len(stack) < 2:
                return False
            stack.pop()
            stack.pop()
            stack.push('X')
        else:
            return False
    return len(stack) == 1


# -- Conversion Functions --

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