import re

class Stack:
    """This is a stack interface class that provides
    basic stack operations and conceals other list operations.
    """
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop(-1)

    def peek(self):
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return str(self.stack)


# Helper functions for use in the conversion functions
def is_operator(token):
    return token in ['+', '-', '*', '/']

def strip_whitespace(expression):
    return expression.replace(' ', '')

def is_operator(c):
    return c in {'+', '-', '*', '/', '^'}

def is_operand(c):
    return c.isdigit() or c.isalpha()  # Digits or variables

# Validation functions for infix, prefix, and postfix expressions
def has_valid_parentheses(expression):
    """Check if the expression has valid parentheses"""
    stack = Stack()
    matching_parentheses = {')': '(', ']': '[', '}': '{', '>': '<'}
    for char in expression:
        if char in matching_parentheses.values():  # Opening parentheses
            stack.push(char)
        elif char in matching_parentheses.keys():  # Closing parentheses
            if not stack or stack.pop() != matching_parentheses[char]:
                return False
    return not stack  # True if stack is empty

def validate_infix(expression):
    """Check if the infix expression is valid"""
    pattern = re.compile(r'^[A-Z\+\-\*\/\(\)\[\]\{\}\<\>\s]*$')
    if not pattern.match(expression):
        return False
    if not has_valid_parentheses(expression):
        return False
    prev_char = ''
    for char in expression:
        if is_operator(char) and (is_operator(prev_char) or prev_char == '(' or prev_char == ''):
            return False
        if is_operand(char) and is_operand(prev_char):
            return False
        prev_char = char

    return not (is_operator(prev_char) or prev_char == '')

def validate_prefix(expression):
    """Check if the prefix expression is valid"""
    pattern = re.compile(r'^[A-Z\+\-\*\/\^\s]*$')
    if not pattern.match(expression):
        return False
    stack = Stack()
    for char in reversed(expression.split()):
        if is_operand(char):
            stack.push(char)
        elif is_operator(char):
            if len(stack) < 2:
                return False
            stack.pop()
            stack.pop()
            stack.push('x')  # Push a dummy operand
    return len(stack) == 1

def validate_postfix(expression):
    """Check if the postfix expression is valid"""
    pattern = re.compile(r'^[A-Z\+\-\*\/\^\s]*$')
    if not pattern.match(expression):
        return False
    stack = Stack()
    for char in expression.split():
        if is_operand(char):
            stack.push(char)
        elif is_operator(char):
            if len(stack) < 2:
                return False
            stack.pop()
            stack.pop()
            stack.push('x')  # Push a dummy operand
    return len(stack) == 1


def prefix_to_infix(expression):
    """Convert prefix expression to infix"""
    if not validate_prefix(expression):
        raise ValueError('Invalid expression')
    stack = Stack()
    for token in reversed(expression):
        if is_operator(token):
            operand1 = stack.pop()
            operand2 = stack.pop()
            stack.push(f'({operand1} {token} {operand2})')
        else:
            stack.push(token)
    return stack.peek()


def infix_to_prefix(expression):
    """Convert infix expression to prefix"""
    if not validate_infix(expression):
        raise ValueError('Invalid expression')
    stack = Stack()
    for token in expression:
        if is_operator(token):
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.push(f'{token}{operand1}{operand2}')
        else:
            stack.push(token)
    result = stack.pop()
    if not stack.is_empty():
        raise ValueError('Invalid expression')
    if not validate_prefix(result):
        raise ValueError('Invalid expression')
    return result

def infix_to_postfix(expression):
    """Convert infix expression to postfix"""
    if not validate_infix(expression):
        raise ValueError('Invalid expression')
    try:
        stack = Stack()
        for token in expression:
            if is_operator(token):
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.push(f'{operand1}{operand2}{token}')
            else:
                stack.push(token)
    except:
        raise ValueError('Invalid expression')
    result = stack.pop()
    if not stack.is_empty():
        raise ValueError(f"Invalid expression. Traceback: stack is not empty. Stack: {stack}")
    if not validate_postfix(result):
        raise ValueError('Invalid expression')
    return result

def postfix_to_infix(expression):
    """Convert postfix expression to infix"""
    if not validate_postfix(expression):
        raise ValueError('Invalid expression')
    try:
        stack = Stack()
        for token in expression:
            if is_operator(token):
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.push(f'({operand1} {token} {operand2})')
            else:
                stack.push(token)
    except:
        raise ValueError('Invalid expression')
    result = stack.pop()
    if not stack.is_empty():
        raise ValueError('Invalid expression')
    if not validate_infix(result):
        raise ValueError('Invalid expression')
    return result

def prefix_to_postfix(expression):
    """Convert prefix expression to postfix"""
    return infix_to_postfix(prefix_to_infix(expression))

def postfix_to_prefix(expression):
    """Convert postfix expression to prefix"""
    return infix_to_prefix(postfix_to_infix(expression))

