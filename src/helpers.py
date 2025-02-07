import re

# Helper functions

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return str(self.stack)

def is_operator(token):
    return token in ['+', '-', '*', '/']

def strip_whitespace(expression):
    return expression.replace(' ', '')

def validate_expression(expression):
    """Only operators and capital letters are allowed"""
    return re.match(r'^[A-Z\+\-\*\/]+$', expression)

# Main functions

def prefix_to_infix(expression):
    """Convert prefix expression to infix"""
    if not validate_expression(expression):
        raise ValueError('Invalid expression')
    stack = Stack()
    for token in reversed(expression):
        if is_operator(token):
            operand1 = stack.pop()
            operand2 = stack.pop()
            stack.push(f'({operand1} {token} {operand2})')
        else:
            stack.push(token)
    return stack[0]


def infix_to_prefix(expression):
    """Convert infix expression to prefix"""
    if not validate_expression(expression):
        raise ValueError('Invalid expression')
    stack = Stack()
    for token in expression:
        if is_operator(token):
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.push(f'{token}{operand1}{operand2}')
        else:
            stack.push(token)
    return stack[0]

def infix_to_postfix(expression):
    """Convert infix expression to postfix"""
    if not validate_expression(expression):
        raise ValueError('Invalid expression')
    stack = Stack()
    for token in expression:
        if is_operator(token):
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.push(f'{operand1}{operand2}{token}')
        else:
            stack.push(token)
    return stack[0]

def postfix_to_infix(expression):
    """Convert postfix expression to infix"""
    if not validate_expression(expression):
        raise ValueError('Invalid expression')
    stack = Stack()
    for token in expression:
        if is_operator(token):
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.push(f'({operand1} {token} {operand2})')
        else:
            stack.push(token)
    return stack[0]

def prefix_to_postfix(expression):
    """Convert prefix expression to postfix"""
    if not validate_expression(expression):
        raise ValueError('Invalid expression')
    return infix_to_postfix(prefix_to_infix(expression))

def postfix_to_prefix(expression):
    """Convert postfix expression to prefix"""
    if not validate_expression(expression):
        raise ValueError('Invalid expression')
    return infix_to_prefix(postfix_to_infix(expression))

postfix_strings = ["AB + C –", "ABC +-", "AB -C + DEF -+^", "ABCDE -+ ^*EF*-"]

prefix_strings = ["++A - * ^BCD/ + EF * GHI", "+-^ABC * D ** EFG"]

infix_strings = ["(A + B) * (C ^(D-E) + F) – G", "A + (((B-C) * (D-E) + F)/G) ^ (H-J)"]