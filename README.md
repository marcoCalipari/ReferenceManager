# Reference Manager

This tool aids researchers in managing citations consistently when working on collaborative, non-LaTeX documents.

## Important Guidelines

- The tool is optimized for IEEE style citations:
  - Citations should be numbered sequentially ([1], [2], etc.).
  - Titles of papers should be enclosed in quotation marks (" ").
  - Publication dates should be placed at the end of each reference.

Please verify all citation keys manually as the tool may generate incorrect keys for non-IEEE styles.

## Usage Instructions

Prepare the following two files:

1. A "seen_references.txt" file containing all references for the specific section.
2. A "full_text.txt" file containing the full text with citation placeholders.

Run the script using the following command:
`python3 references.py > out.txt`

The output file `out.txt` will contain the dictionary of citation keys and their corresponding references, followed by the full text with the placeholders replaced by the new citation keys.

## Citation Key Generation

1. **Citation Format**:
   - For papers with up to three authors, form the key using the initial of each author’s surname followed by the last two digits of the publication year.
     Examples:
     - J. Doe, M. Mustermann, K. Rossi, Q. Zhi, "A paper", 2024 would be cited as DMR24.
     - J. Doe, "A paper", 2024 would be cited as D24.
     - J. Doe, M. Mustermann, "A paper", 2024 would be cited as DM24.
2. **Rules for Letters**:
   - Use uppercase letters only for the initials of the last names.
   - In cases where duplicate initials occur, differentiate by appending an additional letter (e.g., SM24 might become SMa24 and SMb24 for distinct references).
