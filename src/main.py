import yaml
import os
from pathlib import Path
from collections import deque
from src.converters import (
    infix_to_prefix,
    infix_to_postfix,
    prefix_to_infix,
    prefix_to_postfix,
    postfix_to_infix,
    postfix_to_prefix,
)

CONFIG_PATH = 'src/config.yml'
OUTPUT_DIR = 'outputs'

def get_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def get_data_paths() -> dict:
    config = get_config()
    required_keys = ['base_dir', 'infix_file', 'prefix_file', 'postfix_file']
    if not all(key in config for key in required_keys):
        raise KeyError(f"Config must contain: {required_keys}")
    
    base_dir = Path(os.getcwd()) / config['base_dir']
    
    # Find the actual filenames
    infix_files = list(base_dir.glob(config['infix_file']))
    prefix_files = list(base_dir.glob(config['prefix_file']))
    postfix_files = list(base_dir.glob(config['postfix_file']))
    
    if not (infix_files and prefix_files and postfix_files):
        raise FileNotFoundError(f"Could not find required files in {base_dir}")
        
    return {
        'infix': infix_files[0],  # Take the first matching file
        'prefix': prefix_files[0],
        'postfix': postfix_files[0]
    }

def read_expressions(file_path: Path) -> list:
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def identify_expression(expr: str) -> str:
    expr = expr.strip()
    # If the expression starts with an operator, we assume it's prefix.
    if expr[0] in '+-*/^':
        return 'prefix'
    # If it ends with an operator, we assume it's postfix.
    elif expr[-1] in '+-*/^':
        return 'postfix'
    # Otherwise, it's infix.
    return 'infix'

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