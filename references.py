import re

def parse_citation(citation):
    # Remove leading numbering like [1], [2], etc.
    citation = re.sub(r'^\[\d+\]\s*', '', citation)

    # Try to extract the year
    year_match = re.search(r'\b(19|20)\d{2}\b', citation)
    year = year_match.group() if year_match else 'n.d.'

    # Find where the title starts
    title_start = citation.find('"')
    if title_start == -1:
        title_start_match = re.search(r'\.\s+[A-Z]', citation)
        if title_start_match:
            title_start = title_start_match.start()
        else:
            title_start = len(citation)

    # Extract the authors part
    authors_part = citation[:title_start].strip()

    # Remove any trailing commas or conjunctions
    authors_part = re.sub(r'[\.,]\s*$', '', authors_part)
    return {'authors': authors_part, 'year': year}

def extract_surnames(authors_str):
    # Remove 'et al.' and other common phrases
    authors_str = re.sub(r'\bet al\.?\b', '', authors_str, flags=re.IGNORECASE)
    authors_str = authors_str.strip(', ')

    # Use regex to split authors while keeping 'Surname, Initials' together
    authors = re.split(r',\s+and\s+|\s+and\s+|,\s+|\s+&\s+', authors_str)

    surnames = []
    for author in authors:
        author = author.strip()
        if not author:
            continue
        # If the format includes ',', it's likely 'Surname, Initials'
        if ',' in author:
            surname = author.split(',')[0].strip()
            if not re.match(r'^[A-Z]\.?$', surname, re.IGNORECASE):
                surnames.append(surname)
        else:
            # Split potential 'Initials Surname' format without commas
            parts = author.split()
            if len(parts) > 1:
                possible_surnames = [parts[-1]]
            else:
                possible_surnames = parts
            for part in possible_surnames:
                if not re.match(r'^[A-Z]\.?$', part, re.IGNORECASE):
                    surnames.append(part)
                    break  # Stop after finding the surname

    # Remove duplicates while preserving order
    surnames_unique = []
    seen_surnames = set()
    for surname in surnames:
        if surname not in seen_surnames:
            seen_surnames.add(surname)
            surnames_unique.append(surname)

    return surnames_unique

def extract_surname_initials(authors_str):
    surnames = extract_surnames(authors_str)
    # Get initials from surnames (up to 3)
    initials = ''.join([surname[0].upper() for surname in surnames[:3]])
    return initials

def main(referencesFile,fullTextFile):
    # Generate the citation keys from the reference file
    with open(referencesFile, 'r', encoding='utf-8') as f:
        citations = f.readlines()

    parsed_citations = []
    for citation in citations:
        citation = citation.strip()
        if not citation:
            continue
        parsed = parse_citation(citation)
        if parsed:
            parsed['original'] = citation  # Add original citation
            parsed_citations.append(parsed)

    citation_counts = {}
    citation_dict = {}
    for citation in parsed_citations:
        authors_initials = extract_surname_initials(citation.get('authors', ''))
        year = citation.get('year', 'n.d.')
        last_two_digits = year[-2:] if year != 'n.d.' else 'nd'
        base_citation_key = f"[{authors_initials}{last_two_digits}]"
        count = citation_counts.get(base_citation_key, 0)
        if count == 0:
            citation_counts[base_citation_key] = 1
            citation_key = base_citation_key
        else:
            suffix = chr(ord('a') + count - 1)
            citation_key = f"{base_citation_key}{suffix}"
            citation_counts[base_citation_key] += 1
        # Add to dictionary
        
        citation_dict[citation_key] = citation['original']

    for key in citation_dict:
        citation_dict[key] = re.sub(r'\[\d+\]', '', citation_dict[key])
    # Print the dictionary
    # for key, original_citation in citation_dict.items():
    #     print(f"{key}: {original_citation}\n")
    
    # Now we will parse the full text with old references.
    with open(fullTextFile, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # Now we try to isolate all the references [1], [2], etc.
    references = re.findall(r'\[\d+\]', full_text)
    # print(references)
    # Now we will replace the references in the text with the citation in the form of [citation_key] from the dictionary
    for reference in references:
        citation_number = int(reference[1:-1])
        citation_key = list(citation_dict.keys())[citation_number - 1]
        full_text = full_text.replace(reference, f'{citation_key}')
    for key, original_citation in citation_dict.items():
        print(f"{key}: {original_citation}\n")
    print(full_text)
    

    
    
    

if __name__ == '__main__':
    referencesFile = 'seen_references.txt'
    fullTextFile = 'full_text.txt'
    # Print the dictionary

    main(referencesFile, fullTextFile)
