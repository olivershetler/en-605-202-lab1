from src.converters import *
import os
from datetime import datetime

def set_path():
    """Get the project root directory"""
    # Get the directory containing main.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # The resources directory should be at the same level as src
    return current_dir

def create_output_directory(project_dir):
    """Create timestamped output directory"""
    # Create timestamp in format: YYYY-MM-DD_HH-MM-SS
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Create outputs directory if it doesn't exist
    outputs_dir = os.path.join(project_dir, 'outputs')
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    
    # Create timestamped directory
    timestamped_dir = os.path.join(outputs_dir, timestamp)
    os.makedirs(timestamped_dir)
    
    return timestamped_dir

def read_expression_files(filename):
    """Read the expressions from the text files in the resources/data directory"""
    with open(filename, 'r') as file:
        expressions = file.readlines()
    return expressions

def process_expression_files(expressions, converter_function):
    """Process each expression using the functions in converters.py"""
    results = []
    for expression in expressions:
        try:
            result = converter_function(expression)
            results.append(result)
        except Exception as e:
            results.append(f"Error: {e}")
    return results

def display_results(results, output_filename):
    """Display the results to an output file"""
    with open(output_filename, 'w') as file:
        for result in results:
            file.write(f"{result}\n")

def main():
    # Get project root directory
    project_dir = set_path()
    
    # Create timestamped output directory
    output_dir = create_output_directory(project_dir)
    print(f"Results will be saved to {output_dir}")
    
    # Construct path to data directory
    data_dir = os.path.join(project_dir, 'resources', 'data')
    print(f"Looking for data in {data_dir}")

    # Verify data directory exists
    if not os.path.exists(data_dir):
        print(f"Error: Directory {data_dir} does not exist")
        return

    # Process each .txt file in the data directory
    for filename in os.listdir(data_dir):
        if not filename.endswith('.txt'):
            continue
            
        input_path = os.path.join(data_dir, filename)
        expressions = read_expression_files(input_path)
        base_filename = os.path.splitext(filename)[0]

        # Determine expression type and apply appropriate conversions
        filename_lower = filename.lower()
        if 'prefix' in filename_lower:
            # Convert prefix notation to both infix and postfix
            infix_result = process_expression_files(expressions, prefix_to_infix)
            postfix_result = process_expression_files(expressions, prefix_to_postfix)

            # Write results to timestamped directory
            display_results(infix_result, os.path.join(output_dir, f"{base_filename}_to_infix.txt"))
            display_results(postfix_result, os.path.join(output_dir, f"{base_filename}_to_postfix.txt"))

        elif 'postfix' in filename_lower:
            # Convert postfix notation to both infix and prefix
            infix_result = process_expression_files(expressions, postfix_to_infix)
            prefix_result = process_expression_files(expressions, postfix_to_prefix)

            display_results(infix_result, os.path.join(output_dir, f"{base_filename}_to_infix.txt"))
            display_results(prefix_result, os.path.join(output_dir, f"{base_filename}_to_prefix.txt"))

        elif 'infix' in filename_lower:
            # Convert infix notation to both postfix and prefix
            postfix_result = process_expression_files(expressions, infix_to_postfix)
            prefix_result = process_expression_files(expressions, infix_to_prefix)

            display_results(postfix_result, os.path.join(output_dir, f"{base_filename}_to_postfix.txt"))
            display_results(prefix_result, os.path.join(output_dir, f"{base_filename}_to_prefix.txt"))
        
        else:
            print(f"Skipping {filename} - file type not recognized")
            continue

        print(f"Successfully processed {filename}")

if __name__ == "__main__":
    main()