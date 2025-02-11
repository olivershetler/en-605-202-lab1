import os
from typing import List, Dict
from pathlib import Path

class FileProcessor:
    def __init__(self, input_dir: str = "input_files"):
        self.input_dir = input_dir
        os.makedirs(input_dir, exist_ok=True)
    
    def read_input_files(self) -> List[Dict]:
        """Read all input files and prepare them for processing"""
        input_cases = []
        file_id = 0
        
        # Walk through input directory
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read().strip()
                            
                            # Try to determine expression type from filename
                            expr_type = 'unknown'
                            if 'infix' in file.lower():
                                expr_type = 'infix'
                            elif 'prefix' in file.lower():
                                expr_type = 'prefix'
                            elif 'postfix' in file.lower():
                                expr_type = 'postfix'
                            
                            input_cases.append({
                                'expression': content,
                                'type': expr_type,
                                'thread_id': file_id,
                                'source_file': str(file_path)
                            })
                            file_id += 1
                            
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
        
        return input_cases