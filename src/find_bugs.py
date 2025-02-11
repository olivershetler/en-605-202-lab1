from pathlib import Path
import os
from typing import Dict
from datetime import datetime

class BugTracker:
    def __init__(self):
        self.bugs_dir = self._ensure_bugs_dir()

    def _ensure_bugs_dir(self) -> Path:
        """Create bugs directory if it doesn't exist"""
        bugs_path = Path(os.getcwd()) / 'bugs'
        bugs_path.mkdir(exist_ok=True)
        return bugs_path

    def save_errors(self, conversions_dict: Dict[str, Dict[str, str]], timestamp: str):
        """
        Save all errors to a bugs file
        
        Args:
            conversions_dict: Dictionary containing all conversions
                Format: {
                    'infix': {'prefix': {...}, 'postfix': {...}},
                    'prefix': {'infix': {...}, 'postfix': {...}},
                    'postfix': {'infix': {...}, 'prefix': {...}}
                }
            timestamp: Timestamp string for file naming
        """
        filename = f"conversion_errors_{timestamp}.txt"
        bugs_path = self.bugs_dir / filename
        
        print(f"\nSaving errors to {filename}...")
        
        with open(bugs_path, 'w') as f:
            f.write("Conversion Errors\n")
            f.write("=" * 40 + "\n\n")
            
            # Check each conversion type
            for input_type, conversions in conversions_dict.items():
                f.write(f"{input_type.title()} Expression Errors:\n")
                f.write("-" * 20 + "\n")
                
                # Check each output type
                for output_type, results in conversions.items():
                    has_errors = False
                    for input_expr, output_expr in results.items():
                        if output_expr.startswith('ERROR:'):
                            has_errors = True
                            f.write(f"Converting to {output_type}:\n")
                            f.write(f"Input:  {input_expr}\n")
                            f.write(f"Error:  {output_expr}\n\n")
                    
                    if not has_errors:
                        f.write(f"No errors found for {input_type} to {output_type} conversions\n\n")
                f.write("\n")