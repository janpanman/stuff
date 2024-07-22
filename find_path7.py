import os
import re
import sys

def convert_glob_to_regex(pattern):
    # Convert shell-style glob patterns to regex patterns
    pattern = re.escape(pattern)
    pattern = pattern.replace(r'\*', '.*')  # * matches any sequence of characters
    pattern = pattern.replace(r'\?', '.')   # ? matches any single character
    pattern = pattern.replace(r'\[', '[')  # Preserve character classes
    pattern = pattern.replace(r'\]', ']')
    return '^' + pattern + '$'

def find_matching_path(pattern):
    # Convert glob pattern to regex pattern
    regex_pattern = convert_glob_to_regex(pattern)
    regex = re.compile(regex_pattern)
    
    # Determine if the search starts from root or current directory
    if pattern.startswith('/') or pattern[1:2] == ':':
        current_directories = [os.path.sep]
    else:
        current_directories = ['.']
    
    for directory in current_directories:
        try:
            for entry in os.listdir(directory):
                full_path = os.path.join(directory, entry)
                if regex.match(entry):
                    return full_path  # Return immediately upon finding the first match
        except OSError:
            # Skip directories we don't have permission to access
            continue

    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_path.py <pattern>")
        sys.exit(1)

    pattern = sys.argv[1]
    match = find_matching_path(pattern)
    
    if match:
        print("Path matching the pattern: {0}".format(match))
    else:
        print("No paths match the given pattern.")

