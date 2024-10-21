import re

# This code will parse a full text with references, and stores all the references it sees.
# given the text, we will generate a dictionary of references that have been seen, and for every textchunk, we will first check the dictionary, and if the key is alread inside ot it, we will not add it but just pass
# it will be a function script, not a class

def ReferenceHarmonizer(text):
    with open(fullTextFile, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Now we try to isolate all the reference keys [SSS24], [SF06], etc.
    references = re.findall(r'\[\w+\d+\]', full_text)
    print(references, len(references))
    
    # Now we check if there is the file with the references. In case there is not
    # we will create an empty set, as well as file. In case there is, we will parse it and create the set that represents the current state of the citations.
    try:
        with open('references.txt', 'r', encoding='utf-8') as f:
            seen_citations = f.readlines()
    except FileNotFoundError:
        seen_citations = set()
        with open('references.txt', 'w', encoding='utf-8') as f:
            f.write('')
    
    # We need now to conver the parsed file into a dictionary, where we will have the key as the reference key, and the value as the reference itself.
    elems = [elem.strip() for elem in seen_citations]
    print(elems)
    
    
    # Now we will check if the references keys are already in the set. If they are not, we will add them to the set and the file.
    # for elem in references:
    #     if elem not in seen_citations:
    #         seen_citations.add(elem)
    #         with open('ttt.txt', 'a', encoding='utf-8') as f:
    #             f.write(elem + '\n')
    
    # Now we will parse the 
    
    

    
def main(text):
    ReferenceHarmonizer(text)
    
if __name__ == '__main__':
    fullTextFile = 'out.txt'
    main(fullTextFile)