import os
import shutil

def clean_outputs():
    """Delete all files in the outputs directory"""
    output_dir = "outputs"
    
    try:
        # Check if directory exists
        if os.path.exists(output_dir):
            # Remove all contents of the directory
            shutil.rmtree(output_dir)
            print(f"Successfully cleaned {output_dir} directory")
            
            # Recreate empty outputs directory
            os.makedirs(output_dir)
            print(f"Recreated empty {output_dir} directory")
        else:
            print(f"No {output_dir} directory found")
            
    except Exception as e:
        print(f"Error cleaning outputs: {e}")

if __name__ == "__main__":
    clean_outputs() 