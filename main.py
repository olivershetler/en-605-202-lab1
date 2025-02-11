import yaml
import os
from pathlib import Path
from typing import Dict, List, Callable
from datetime import datetime
from collections import deque

from src.converters import *
from src.find_bugs import BugTracker
from src.prefix_validator import PrefixValidator

CONFIG_PATH = 'src/config.yml'
EXPRESSION_TYPES = ['infix', 'prefix', 'postfix']
OUTPUT_DIR = 'outputs'

def get_config() -> dict:
    try:
        with open(os.getcwd() + '/' + CONFIG_PATH) as f:
            return yaml.safe_load(f)  # safe_load is preferred over load for security
    except FileNotFoundError:
        raise FileNotFoundError("Config file not found in src/config.yaml")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing config file: {e}")

def get_data_paths() -> Dict[str, Path]:
    """
    Retrieves file paths for infix, prefix, and postfix expression files from config.
    
    Returns:
        Dict[str, Path]: Dictionary mapping expression types to their file paths
    
    Raises:
        FileNotFoundError: If config file is not found
        KeyError: If required config keys are missing
    """
    try:
        config = get_config()
        required_keys = ['data_dir', 'infix_file', 'prefix_file', 'postfix_file']
        if not all(key in config for key in required_keys):
            raise KeyError(f"Config must contain: {required_keys}")
        cwd = Path(os.getcwd())
        data_dir = cwd / Path(config['data_dir'])
        infix_path = data_dir / config['infix_file']
        prefix_path = data_dir / config['prefix_file']
        postfix_path = data_dir / config['postfix_file']
        return {
            'infix': infix_path,
            'prefix': prefix_path,
            'postfix': postfix_path
        }
    except Exception as e:
        raise Exception(f"Error getting data paths: {e}")

def read_expressions(file_path: Path) -> List[str]:
    """Read expressions and filter out empty lines"""
    try:
        print(f"Reading expressions from {file_path.name}...")
        with open(file_path, 'r') as f:
            expressions = f.read().split('\n')
            filtered = list(filter(None, expressions))
            print(f"Found {len(filtered)} expressions")
            return filtered
    except FileNotFoundError:
        raise FileNotFoundError(f"Expression file not found: {file_path}")

def format_conversions(expressions: List[str], 
                      converter: Callable[[str], str]) -> Dict[str, str]:
    return dict(zip(expressions, map(converter, expressions)))

def convert_expressions(converter: Callable[[str], str], 
                       expressions: List[str]) -> Dict[str, str]:
    """Convert expressions with error handling"""
    results = {}
    for expr in expressions:
        try:
            results[expr] = converter(expr)
        except Exception as e:
            print(f"Error converting expression '{expr}': {str(e)}")
            results[expr] = "ERROR: " + str(e)
    return results

def format_results(conversions: Dict[str, str]) -> str:
    return '\n'.join([f'{k} -> {v}' for k, v in conversions.items()])

def ensure_output_dir():
    """Create outputs directory if it doesn't exist"""
    output_path = Path(os.getcwd()) / OUTPUT_DIR
    output_path.mkdir(exist_ok=True)
    return output_path

def save_conversions(input_type: str, expressions: Dict[str, str], 
                    output_types: List[str], timestamp: str):
    """
    Save conversion results to files in the outputs directory
    
    Args:
        input_type: The type of input expression (infix/prefix/postfix)
        expressions: Dictionary mapping input expressions to converted expressions
        output_types: List of output expression types
        timestamp: Timestamp string for file naming
    """
    output_dir = ensure_output_dir()
    
    for output_type in output_types:
        if input_type == output_type:
            continue
            
        filename = f"{input_type}_to_{output_type}_{timestamp}.txt"
        output_path = output_dir / filename
        
        print(f"Saving conversion to {filename}...")  # Add debug print
        
        with open(output_path, 'w') as f:
            f.write(f"Input ({input_type}) -> Output ({output_type})\n")
            f.write("=" * 40 + "\n")
            for input_expr, output_expr in expressions.items():
                f.write(f"{input_expr} -> {output_expr}\n")

def standardize_expression(expr):
    """
    Standardizes input expression by normalizing operators and removing whitespace.
    Handles various dash characters and double negatives.
    """
    # Normalize different dash characters to standard minus
    expr = expr.replace('–', '-').replace('—', '-').replace('−', '-')
    
    # Convert double negatives to addition
    expr = expr.replace('--', '+')
    
    # Remove whitespace and quotes for processing
    expr = ''.join(expr.split())
    expr = expr.replace('"', '')
    
    # Filter to retain only valid expression characters
    return ''.join(c for c in expr if c.isalnum() or c in '+-*/^()' or c == '-')

def identify_expression_type(expression):
    """
    Determines expression notation type based on operator placement and structure.
    Returns: 'infix', 'prefix', 'postfix', or 'unknown'
    """
    if not expression:
        return "unknown"
    
    tokens = list(expression)
    
    # Check for infix notation indicators
    if '(' in tokens:
        return "infix"
    
    # Validate prefix notation
    if tokens[0] in OPERATORS:
        try:
            if validate_prefix(expression):
                return "prefix"
        except:
            pass
            
    # For postfix expressions, last character must be an operator
    if tokens[-1] in OPERATORS:
        try:
            if validate_postfix(expression):
                return "postfix"
        except:
            pass
    
    # Try infix validation last (for expressions without parentheses)
    try:
        if validate_infix(expression):
            return "infix"
    except:
        pass
        
    return "unknown"

def write_and_print(message, output_file=None):
    """Write to both console and file"""
    print(message)
    if output_file:
        output_file.write(message + "\n")

def analyze_expression(expr):
    """
    Analyzes and standardizes any expression, determining its type automatically.
    Returns (standardized_expression, type)
    """
    # Clean the expression
    std_expr = ''.join(c for c in expr if c.isalnum() or c in '+-*/^()' or c in '–—−')
    
    # Determine type based on structure
    if std_expr[0] in '+-*/^':
        return std_expr, 'prefix'
    elif std_expr[-1] in '+-*/^':
        return std_expr, 'postfix'
    else:
        return std_expr, 'infix'

def validate_infix_structure(expr):
    """Basic validation of infix expression structure"""
    try:
        # Check for operator between operands
        tokens = [c for c in expr if c not in '()']
        for i in range(len(tokens)-1):
            if tokens[i].isalnum() and tokens[i+1].isalnum():
                return False
            if (tokens[i] in '+-*/^') and (tokens[i+1] in '+-*/^'):
                return False
        return True
    except:
        return False

def standardize_for_comparison(expr):
    """Standardize expression for comparison by removing spaces and parentheses"""
    return ''.join(c for c in expr if c not in '() ')

class ExpressionStacks:
    def __init__(self):
        self.infix_stack = deque()
        self.prefix_stack = deque()
        self.postfix_stack = deque()
    
    def add_expression(self, expr, expr_type):
        """Add expression to appropriate stack based on type"""
        if expr_type == 'infix':
            self.infix_stack.append(expr)
        elif expr_type == 'prefix':
            self.prefix_stack.append(expr)
        elif expr_type == 'postfix':
            self.postfix_stack.append(expr)
    
    def verify_infix(self, expr):
        """Verify infix expression"""
        try:
            # Remove spaces and check structure
            clean_expr = ''.join(expr.split())
            
            # Must contain operators between operands
            for i in range(len(clean_expr)-1):
                if clean_expr[i].isalnum() and clean_expr[i+1].isalnum():
                    return False
                    
            # Check balanced parentheses
            if clean_expr.count('(') != clean_expr.count(')'):
                return False
                
            return True
        except:
            return False
    
    def verify_prefix(self, expr):
        """Verify prefix expression"""
        try:
            # Remove spaces and check structure
            clean_expr = ''.join(expr.split())
            
            # Must start with operator
            if not clean_expr[0] in '+-*/^':
                return False
                
            # Count operators and operands
            operators = [c for c in clean_expr if c in '+-*/^']
            operands = [c for c in clean_expr if c.isalnum()]
            
            # For prefix: operands = operators + 1
            return len(operands) == len(operators) + 1
        except:
            return False
    
    def verify_postfix(self, expr):
        """Verify postfix expression"""
        try:
            # Remove spaces and check structure
            clean_expr = ''.join(expr.split())
            
            # Must end with operator
            if not clean_expr[-1] in '+-*/^':
                return False
                
            # Count operators and operands
            operators = [c for c in clean_expr if c in '+-*/^']
            operands = [c for c in clean_expr if c.isalnum()]
            
            # For postfix: operands = operators + 1
            return len(operands) == len(operators) + 1
        except:
            return False
    
    def verify_stacks(self, output_file=None):
        """Verify each expression is in the correct stack"""
        def write_and_print(message):
            print(message)
            if output_file:
                output_file.write(message + "\n")
        
        write_and_print("\nVerifying Expression Stacks:")
        write_and_print("=" * 50)
        
        # Verify infix stack
        write_and_print("\nInfix Stack Verification:")
        for expr in self.infix_stack:
            is_valid = self.verify_infix(expr)
            write_and_print(f"  {expr}: {is_valid}")
        
        # Verify prefix stack
        write_and_print("\nPrefix Stack Verification:")
        for expr in self.prefix_stack:
            is_valid = self.verify_prefix(expr)
            write_and_print(f"  {expr}: {is_valid}")
        
        # Verify postfix stack
        write_and_print("\nPostfix Stack Verification:")
        for expr in self.postfix_stack:
            is_valid = self.verify_postfix(expr)
            write_and_print(f"  {expr}: {is_valid}")
    
    def print_stacks(self, output_file=None):
        """Print contents of all stacks"""
        def write_and_print(message):
            print(message)
            if output_file:
                output_file.write(message + "\n")
        
        write_and_print("\nExpression Stacks:")
        write_and_print("=" * 50)
        write_and_print("\nInfix Stack:")
        for expr in self.infix_stack:
            write_and_print(f"  {expr}")
        
        write_and_print("\nPrefix Stack:")
        for expr in self.prefix_stack:
            write_and_print(f"  {expr}")
        
        write_and_print("\nPostfix Stack:")
        for expr in self.postfix_stack:
            write_and_print(f"  {expr}")

def process_expression(expr, output_file, stacks):
    """Process a single expression and store conversions in stacks"""
    try:
        std_expr, expr_type = analyze_expression(expr)
        
        write_and_print(f"\nOriginal Expression: {expr}", output_file)
        write_and_print(f"Detected Type: {expr_type}", output_file)
        
        if expr_type == 'infix':
            prefix_ver = infix_to_prefix(std_expr)
            postfix_ver = infix_to_postfix(std_expr)
            write_and_print(f"To Prefix:  {prefix_ver}", output_file)
            write_and_print(f"To Postfix: {postfix_ver}", output_file)
            
            # Add to stacks
            stacks.add_expression(std_expr, 'infix')
            stacks.add_expression(prefix_ver, 'prefix')
            stacks.add_expression(postfix_ver, 'postfix')
            
        elif expr_type == 'prefix':
            infix_ver = prefix_to_infix(std_expr)
            postfix_ver = prefix_to_postfix(std_expr)
            write_and_print(f"To Infix:   {infix_ver}", output_file)
            write_and_print(f"To Postfix: {postfix_ver}", output_file)
            
            # Add to stacks
            stacks.add_expression(infix_ver, 'infix')
            stacks.add_expression(std_expr, 'prefix')
            stacks.add_expression(postfix_ver, 'postfix')
            
        elif expr_type == 'postfix':
            infix_ver = postfix_to_infix(std_expr)
            prefix_ver = postfix_to_prefix(std_expr)
            write_and_print(f"To Infix:   {infix_ver}", output_file)
            write_and_print(f"To Prefix:  {prefix_ver}", output_file)
            
            # Add to stacks
            stacks.add_expression(infix_ver, 'infix')
            stacks.add_expression(prefix_ver, 'prefix')
            stacks.add_expression(std_expr, 'postfix')
            
    except Exception as e:
        write_and_print(f"Error processing expression: {e}", output_file)

def process_file(input_filepath):
    """Process all expressions in a file"""
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    input_filename = os.path.basename(input_filepath)
    output_filename = f"converted_{input_filename}"
    output_filepath = os.path.join(output_dir, output_filename)
    
    # Create stacks for this file
    stacks = ExpressionStacks()
    
    write_and_print(f"\nProcessing {input_filename}")
    write_and_print("=" * 50)
    
    try:
        with open(input_filepath, 'r') as infile, open(output_filepath, 'w') as outfile:
            outfile.write(f"Results for {input_filename}\n")
            outfile.write("=" * 50 + "\n")
            
            expressions = [line.strip() for line in infile if line.strip()]
            for expr in expressions:
                process_expression(expr, outfile, stacks)
            
            # Print stack contents at the end
            stacks.print_stacks(outfile)
            stacks.verify_stacks(outfile)
                
    except FileNotFoundError:
        write_and_print(f"Error: File {input_filepath} not found")
    
    return stacks

def main():
    data_dir = "resources/data"
    files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    
    write_and_print("\nStarting Expression Conversion Process")
    write_and_print("=" * 50)
    
    all_stacks = []
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        file_stacks = process_file(filepath)
        all_stacks.append(file_stacks)
    
    write_and_print("\nConversion Process Complete")
    write_and_print("=" * 50)

if __name__ == "__main__":
    main()
