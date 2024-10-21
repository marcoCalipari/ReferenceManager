import re
from collections import defaultdict

def ReferenceHarmonizer(full_text_file, references_file='references.txt'):
    """
    Parses the full text to extract reference keys and updates the references file accordingly.
    Checks for duplicate reference keys in the references file.

    Args:
        full_text_file (str): Path to the file containing the full text.
        references_file (str): Path to the references file. Defaults to 'references.txt'.
    
    Returns:
        dict: A dictionary of reference keys and their corresponding citations.
    """
    # Read the full text from the specified file
    try:
        with open(full_text_file, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{full_text_file}' does not exist.")
        return {}
    
    # Extract all reference keys using regex (e.g., [SSS24], [SF06])
    references = re.findall(r'\[\w+\d+\]', full_text)
    print(f"Found {len(references)} references: {references}")
    
    # Initialize a dictionary to store citation counts for duplicate detection
    citation_counts = defaultdict(int)
    
    # Initialize a set to store seen citation keys
    seen_citations = set()
    
    # Initialize the citation dictionary
    citation_dict = {}
    
    # Try to read existing references from the references file
    try:
        with open(references_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():  # Ensure the line is not empty
                    parts = line.strip().split(':', 1)
                    if len(parts) != 2:
                        print(f"Invalid line format (skipped): {line.strip()}")
                        continue
                    key, citation = parts
                    key = key.strip()
                    citation = citation.strip()
                    citation_counts[key] += 1
                    if citation_counts[key] > 1:
                        print(f"Duplicate found in references file: {key}")
                    else:
                        seen_citations.add(key)
                        citation_dict[key] = citation
    except FileNotFoundError:
        # If the references file doesn't exist, create it
        with open(references_file, 'w', encoding='utf-8') as f:
            pass  # Creates an empty file
        print(f"Created new references file: '{references_file}'")
    
    # Prepare to append new references
    new_references = [ref for ref in references if ref not in seen_citations]
    
    if new_references:
        with open(references_file, 'a', encoding='utf-8') as f:
            for ref in new_references:
                f.write(f"{ref}: \n")  # Placeholder for citation details
        print(f"Added {len(new_references)} new references to '{references_file}'.")
    else:
        print("No new references to add.")
    
    # Populate the citation dictionary with any newly added references
    for ref in new_references:
        citation_dict[ref] = ""
    
    return citation_dict

def main():
    full_text_file = 'out.txt'  # Replace with your actual file path
    references_file = 'references.txt'  # You can change this if needed

    citations = ReferenceHarmonizer(full_text_file, references_file)
    print("\nCurrent Citations Dictionary:")
    for key, citation in citations.items():
        print(f"{key}: {citation}")

if __name__ == '__main__':
    main()
