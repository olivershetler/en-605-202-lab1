from src.converters import *
from collections import deque
from pathlib import Path
import os

class ExpressionStacks:
    def __init__(self):
        self.stacks = {
            'infix': deque(),
            'prefix': deque(),
            'postfix': deque()
        }
    
    def add(self, expr: str, expr_type: str):
        self.stacks[expr_type].append(expr)
    
    def print_all(self):
        print("\nContents of Expression Stacks:")
        for typ in ['infix', 'prefix', 'postfix']:
            print(f"\n{typ.capitalize()} Stack:")
            for expr in self.stacks[typ]:
                print(expr)

def process_expression(expr: str, original_type: str, stacks: ExpressionStacks):
    # Add original expression to its stack
    stacks.add(expr.strip(), original_type)
    
    try:
        if original_type == 'infix':
            # Convert infix to others
            prefix_expr = infix_to_prefix(expr)
            postfix_expr = infix_to_postfix(expr)
            stacks.add(prefix_expr, 'prefix')
            stacks.add(postfix_expr, 'postfix')
            
        elif original_type == 'prefix':
            # Convert prefix to others
            infix_expr = prefix_to_infix(expr)
            postfix_expr = prefix_to_postfix(expr)
            stacks.add(infix_expr, 'infix')
            stacks.add(postfix_expr, 'postfix')
            
        elif original_type == 'postfix':
            # Convert postfix to others
            infix_expr = postfix_to_infix(expr)
            prefix_expr = postfix_to_prefix(expr)
            stacks.add(infix_expr, 'infix')
            stacks.add(prefix_expr, 'prefix')
            
    except Exception as e:
        print(f"Error converting expression '{expr}': {e}")

def main():
    data_dir = Path('resources/data')
    stacks = ExpressionStacks()
    
    # Process all files in the data directory
    for file_path in data_dir.iterdir():
        if file_path.is_file():
            # Determine expression type from filename
            filename = file_path.name.lower()
            if 'infix' in filename:
                expr_type = 'infix'
            elif 'prefix' in filename:
                expr_type = 'prefix'
            elif 'postfix' in filename:
                expr_type = 'postfix'
            else:
                continue  # Skip files that don't match any type
            
            # Read and process expressions from the file
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        if line.strip():
                            process_expression(line.strip(), expr_type, stacks)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
    
    # Print all stacks
    stacks.print_all()

if __name__ == '__main__':
    main()