import os
import re
import sys

def find_matching_path(regex_path):
    # Split the regex path into components
    path_components = regex_path.strip('/\\').split(os.path.sep)
    
    # Determine if the search starts from root or current directory
    if regex_path.startswith(('/', '\\')) or (len(path_components) > 0 and re.match(r'^[a-zA-Z]:', path_components[0])):
        current_directories = [os.path.sep]
    else:
        current_directories = ['.']
    
    for component in path_components:
        next_paths = []
        regex = re.compile(component)
        
        for directory in current_directories:
            try:
                for entry in os.listdir(directory):
                    full_path = os.path.join(directory, entry)
                    if regex.match(entry):
                        next_paths.append(full_path)
            except PermissionError:
                # Skip directories we don't have permission to access
                continue
        
        if not next_paths:
            return None
        
        current_directories = next_paths

    return current_directories

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_path.py <regex_path>")
        sys.exit(1)

    regex_path = sys.argv[1]
    matches = find_matching_path(regex_path)
    
    if matches:
        print("Paths matching the pattern:")
        for match in matches:
            print(match)
    else:
        print("No paths match the given pattern.")

