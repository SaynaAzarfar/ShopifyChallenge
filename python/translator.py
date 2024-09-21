import sys


# Define the Braille mappings
BRAILLE_ALPHABET = {
    'a': "O.....", 'b': "O.O...", 'c': "OO....", 'd': "OO.O..", 'e': "O..O..",
    'f': "OOO...", 'g': "OOOO..", 'h': "O.OO..", 'i': ".OO...", 'j': ".OOO..",
    'k': "O...O.", 'l': "O.O.O.", 'm': "OO..O.", 'n': "OO.OO.", 'o': "O..OO.",
    'p': "OOO.O.", 'q': "OOOOO.", 'r': "O.OOO.", 's': ".OO.O.", 't': ".OOOO.",
    'u': "O...OO", 'v': "O.O.OO", 'w': ".OOO.O", 'x': "OO..OO", 'y': "OO.OOO",
    'z': "O..OOO", 'capital': ".....O", 'number': ".O.OOO",
    '1': "O.....", '2': "O.O...", '3': "OO....", '4': "OO.O..", '5': "O..O..",
    '6': "OOO...", '7': "OOOO..", '8': "O.OO..", '9': ".OO...", '0': ".OOO.."
}

# Reverse dictionary for Braille to English
ENGLISH_ALPHABET = {v: k for k, v in BRAILLE_ALPHABET.items()if k not in ('0','1','2','3','4','5','6','7','8','9')}
NUMBER_ALPHABET = {v: k for k, v in BRAILLE_ALPHABET.items() if k in ('0','1','2','3','4','5','6','7','8','9')}

def detect_and_translate(input_string):
    """
    Automatically detects the type of input (English or Braille) and translates accordingly.
    """
    if all(char in 'O. ' for char in input_string):  # Detect if the input is Braille
        return translate_to_english(input_string)
    else:  # Otherwise, it's assumed to be English
        return translate_to_braille(input_string)


def translate_to_braille(text):
    """
    Translates an English text string to Braille.
    """
    output = []
    number_mode = False

    for char in text:
        if char.isupper():
            output.append(BRAILLE_ALPHABET['capital'])
            output.append(BRAILLE_ALPHABET[char.lower()])
            number_mode = False  # Exit number mode if a letter appears
        elif char.isdigit():
            if not number_mode:  # Add number prefix only once before the first digit
                output.append(BRAILLE_ALPHABET['number'])
                number_mode = True
            output.append(BRAILLE_ALPHABET[char])
        elif char == ' ':
            output.append("......")  # Use visual representation for spaces

        else:
            output.append(BRAILLE_ALPHABET[char])
            number_mode = False  # Exit number mode if a letter appears
    return ''.join(output)


def translate_to_english(braille_text):
    """
    Translates a Braille string to English.
    """
    output = []
    i = 0
    capitalize_next = False
    number_mode = False

    while i < len(braille_text):
        # Read the next 6 characters (1 Braille character)
        braille_char = braille_text[i:i+6]

        if braille_char == BRAILLE_ALPHABET['capital']:
            capitalize_next = True
            i += 6
            # Move to the next Braille character
            continue
        elif braille_char == BRAILLE_ALPHABET['number']:
            number_mode = True
            i += 6  # Move to the next Braille character
            continue
        elif braille_char == "......":  # Handle space representation
            output.append(' ')  # Append space for the Braille space
            i += 6  # Move to the next Braille character
            continue
        else:
            # Convert Braille to English using the ENGLISH_ALPHABET map
            char = ENGLISH_ALPHABET.get(braille_char)

            if char is not None:
                # Handle capitalization
                if capitalize_next:
                    char = char.upper()
                    capitalize_next = False  # Reset the capitalize flag

                # Handle number mode
                if number_mode:
                    # If it's a valid number, append as a digit
                    char = NUMBER_ALPHABET.get(braille_char)
                    if char.isdigit():
                        output.append(char)
                    else:
                        number_mode = False  # Exit number mode if it's not a digit
                        output.append(char)  # Append the character
                else:
                    output.append(char)  # Append regular character if not in number mode
            i += 6  # Move to the next Braille character
    return ''.join(output)


def main():




    input_string =' '.join(sys.argv[1:])
    #
    # # Translate the input based on its type (handled within detect_and_translate)
    result = detect_and_translate(input_string)

    # Output the result
    print(result)


if __name__ == "__main__":
    main()


