import yaml
import os
from pathlib import Path
from typing import Dict, List, Callable
from datetime import datetime

from src.converters import *
from src.find_bugs import BugTracker

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

def main():
    print("Starting expression conversion process...")
    paths = get_data_paths()
    try:
        # Generate timestamp for file names
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("\nReading input files:")
        print("-" * 40)
        infix_expressions = read_expressions(paths['infix'])
        prefix_expressions = read_expressions(paths['prefix'])
        postfix_expressions = read_expressions(paths['postfix'])

        print("\nConverting expressions:")
        print("-" * 40)
        
        print("\nProcessing prefix expressions...")
        prefix_to_others = {
            'infix': convert_expressions(prefix_to_infix, prefix_expressions),
            'postfix': convert_expressions(prefix_to_postfix, prefix_expressions)
        }
        
        print("\nProcessing infix expressions...")
        infix_to_others = {
            'prefix': convert_expressions(infix_to_prefix, infix_expressions),
            'postfix': convert_expressions(infix_to_postfix, infix_expressions)
        }
        
        print("\nProcessing postfix expressions...")
        postfix_to_others = {
            'infix': convert_expressions(postfix_to_infix, postfix_expressions),
            'prefix': convert_expressions(postfix_to_prefix, postfix_expressions)
        }
        # Format results for console output as before
        infix_from_prefix = format_results(prefix_to_others['infix'])
        infix_from_postfix = format_results(postfix_to_others['infix'])
        postfix_from_infix = format_results(infix_to_others['postfix'])
        postfix_from_prefix = format_results(prefix_to_others['postfix'])
        prefix_from_infix = format_results(infix_to_others['prefix'])
        prefix_from_postfix = format_results(postfix_to_others['prefix'])

        # Add explicit saves for each conversion type
        print("\nSaving conversion results...")
        
        # Save prefix conversions
        save_conversions('prefix', prefix_to_others['infix'], ['infix'], timestamp)
        save_conversions('prefix', prefix_to_others['postfix'], ['postfix'], timestamp)
        
        # Save infix conversions
        save_conversions('infix', infix_to_others['prefix'], ['prefix'], timestamp)
        save_conversions('infix', infix_to_others['postfix'], ['postfix'], timestamp)
        
        # Save postfix conversions
        save_conversions('postfix', postfix_to_others['infix'], ['infix'], timestamp)
        save_conversions('postfix', postfix_to_others['prefix'], ['prefix'], timestamp)

        # Track bugs using the new BugTracker class
        bug_tracker = BugTracker()
        bug_tracker.save_errors({
            'infix': infix_to_others,
            'prefix': prefix_to_others,
            'postfix': postfix_to_others
        }, timestamp)

        # Format a string to print the results
        result = f"""Infix from Prefix:
{infix_from_prefix}

Infix from Postfix:
{infix_from_postfix}

Postfix from Infix:
{postfix_from_infix}

Postfix from Prefix:
{postfix_from_prefix}

Prefix from Infix:
{prefix_from_infix}

Prefix from Postfix:
{prefix_from_postfix}

Results have been saved to the '{OUTPUT_DIR}' directory with timestamp {timestamp}
"""
        print(result)
    except Exception as e:
        print(f"Error processing expressions: {e}")
        return

if __name__ == '__main__':
    main()
