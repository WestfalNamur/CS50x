# =============================================================================
# Calcualte Coleman-Liau formula of a user input and return it;
# =============================================================================

import string

from cs50 import get_string


# Prompt for user input
text_str = get_string("Text: ")


# Count variables
n_letters = 0
n_words = 1  # " " seperates words, so 1st word is not counted;
n_sentences = 0


# Loop over string and increment counts according to thier occurences.
for letter in text_str:

    # any occurrence of a period, exclamation point, or question mark indicates
    # the end of a sentence;
    if letter in ["!", "?", "."]:
        n_sentences += 1

    # Ignore special characters
    elif letter in string.punctuation:
        continue

    # any sequence of characters separated by spaces should count as a word;
    elif letter in string.whitespace:
        n_words += 1

    # Everything else is treated as a letter;
    else:
        n_letters += 1


# Caluclate factors and coleman liau index
factor_words = n_words / 100
L = n_letters / factor_words
S = n_sentences / factor_words
coleman_liau_index = round(0.0588 * L - 0.296 * S - 15.8)


# Return
if coleman_liau_index < 1:
    print("Before Grade 1")
elif coleman_liau_index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {coleman_liau_index}")
