# All code here was written by MIBbrandon on Github and has been modified 
# to work as a .py file
# https://github.com/MIBbrandon/Koiwriter


import json
from pathlib import Path
from typing import List, Union


# Some constants pertaining to image parameters have been added here
VIEW_BOX_VAL = 500
VIEW_BOX_VAL2 = 500
SCALE_VALUE = 0.65


def rules_for_tokens(word: str) -> List[str]:
    """All the words in Koilang only have at most two characters to represent a ripple, 
    and it's either a vowel or "h", so separating a word into tokens that can map to
    the ripples is very straightforward. If the language evolves with more complex rules,
    I recommend switching to using a parser like PEST or something similar.

    Args:
        word (str): Word to tokenize

    Returns:
        List[str]: List of tokens as strings
    """
    def both_chars_go_together(char_before: str, char_now: str) -> bool:
        # CONSONANTS
        # Ending in 'h'
        if char_now == 'h' and char_before in ['c', 'k', 'p', 's', 't', 'v', ]:
            return True
        # Ending in 's'
        if char_now == 's' and char_before in ['t']:
            return True
        
        # VOWELS
        # Ending in 'e'
        if char_now == 'e' and char_before in ['a']:
            return True
        
        # Ending in 'i'
        if char_now == 'i' and char_before in ['a', 'i', 'o']:
            return True
        
        # Ending in 'e'
        if char_now == 'u' and char_before in ['a', 'e']:
            return True

        # None of the previous conditions where met
        return False
    word = word.strip().lower()
    
    tokens = []
    
    # Start at second char
    i = 1
    word_length = len(word)
    last_char_index = word_length - 1
    while i < word_length:
        
        char_before = word[i-1]
        char_now = word[i]
        
        # Add both chars as one token or just add char_before
        if both_chars_go_together(char_before, char_now):
            tokens.append(f'{char_before}{char_now}')
            
            if i + 1 == last_char_index:  # If only one char left after char_now
                tokens.append(word[i+1])  # Just add that last char
                break  # End tokenizing
            else:
                i += 1  # Skip char_now becoming char_before in the next iteration
            
        else:
            tokens.append(char_before)  # Add char normally
            if i == last_char_index:  # If char_now is the last char in the word
                tokens.append(char_now)
        
        i += 1
    
    return tokens


# In the original repo, all the following code was in the global scope
# It has been moved into a function for ease-of-use by Rushk
def rippler(word: str):
    tokens = rules_for_tokens(word)
    # tokens = rules_for_tokens("Tsevhu")
    for i, t in enumerate(tokens):
        if t == "'":
            tokens[i] = "`"
    
    # Get density data
    with open(Path("extensions/tsevhu/koiwriter/ripples/density_data.json")) as f:
        density_data = json.loads(f.read())
    
    translate_orientation = {
        "0": {
            "N": "N",
            "NE": "NE",
            "E": "E",
            "SE": "SE",
            "S": "S",
            "SW": "SW",
            "W": "W",
            "NW": "NW"
        },
        "1": {
            "N": "E",
            "NE": "SE",
            "E": "S",
            "SE": "SW",
            "S": "W",
            "SW": "NW",
            "W": "N",
            "NW": "NE"
        },
        "2": {
            "N": "S",
            "NE": "SW",
            "E": "W",
            "SE": "NW",
            "S": "N",
            "SW": "NE",
            "W": "E",
            "NW": "SE"
        },
        "3": {
            "N": "W",
            "NE": "NW",
            "E": "N",
            "SE": "NE",
            "S": "E",
            "SW": "SE",
            "W": "S",
            "NW": "SW"
        },
    }

    # Choose orientations based on densities
    orientations = []  
    previous_dense_above_dir = None
    previous_quarters = None

    for i, token in enumerate(tokens):
        if i == 0:
            # Only need to record dense above direction as is. The first token is never rotated.
            previous_dense_above_dir: List[str] = density_data[token]['dense_above_dir']
            previous_quarters: int = density_data[token]['quarters']
            orientations.append(0)
            continue
        
        # Have a temporary orientation which starts where the previous ripple ended
        temp_orientation = (orientations[i-1] + previous_quarters) % 4
        
        # CHOOSE ORIENTATION BASE ON DENSITY
        # Where it is dense below, it must not coincide with where the previous one is dense above
        dense_below_dir: List[str] = density_data[token]['dense_below_dir']
        chosen_orientation = 0
        for orientation in range(4):
            temp_dense_below_dir = [translate_orientation[str((orientation + temp_orientation) % 4)][d] for d in dense_below_dir]
            
            # Check intersection. Assumes orientation choices have been taken into consideration
            common_dirs = set(temp_dense_below_dir).intersection(set(previous_dense_above_dir))
            if not common_dirs:
                # No clash, valid orientation found
                chosen_orientation = (orientation + temp_orientation) % 4
                break
        
        orientations.append(chosen_orientation)
        
        # Keep information to help next token orientation
        previous_dense_above_dir = [translate_orientation[str(chosen_orientation)][d] for d in density_data[token]['dense_above_dir']]
        previous_quarters: int = density_data[token]['quarters']

    from xml.dom.minidom import parse

    global VIEW_BOX_VAL, VIEW_BOX_VAL2, SCALE_VALUE


    # Create the output file
    with open(Path("extensions/tsevhu/koiwriter/output.svg"), 'w') as output_f:
        view_box_val = VIEW_BOX_VAL
        view_box_val2 = VIEW_BOX_VAL2
        output_f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{view_box_val}" height="{view_box_val}" viewBox="0 0 {view_box_val2} {view_box_val2}">\n')
        
        # Obtain the SVG files for the tokens and add it to the image
        num_tokens = len(tokens)
        for i, token in enumerate(tokens):
            doc = parse(str(Path(f"extensions/tsevhu/koiwriter/ripples/images/{token}.svg")))
            scale_value = SCALE_VALUE ** (num_tokens - (i + 1))
            
            output_f.write(f'\t<g id="{token}_{i}" transform-origin="250 250" transform="scale({scale_value}) rotate({90 * orientations[i]})">\n')
            for child_elem in doc.getElementsByTagName("path"):
                output_f.write(f'\t\t{child_elem.toprettyxml()}\n')
            output_f.write(f'\t</g>\n')
        
        # Added by Xorol to show the original word in the bottom-left
        output_f.write(f'<text x="0" y="100%" textLength="50%">{word}</text>\n')
        
        output_f.write('</svg>\n')