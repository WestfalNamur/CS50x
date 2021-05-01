# An STR is a short sequence of DNA bases that tends to repeat consecutively
# numerous times at specific locations inside of a person’s DNA. The
# number of times any particular STR repeats varies a lot among individuals.
# In the DNA samples below, for example, Alice has the STR AGAT repeated four
# times in her DNA, while Bob has the same STR repeated five times.
#
# In the DNA samples below, for example, Alice has the STR AGAT repeated
# four times in her DNA, while Bob has the same STR repeated five times.
#   Alice:  CTAGATAGATAGATGACTA
#   Bob:    CTAGATAGATAGATAGATAGATT
#
# Specification:
#   1.  * Program should require as its first command-line argument the name of
#       a CSV file containing the STR counts for a list of individuals and
#       should require as its second command-line argument the name of a text
#       file containing the DNA sequence to identify.
#       * If your program is executed with the incorrect number of command-line
#       arguments, your program should print an error message of your choice
#       (with print). If the correct number of arguments are provided, you may
#       assume that the first argument is indeed the filename of a valid CSV file,
#       and that the second argument is the filename of a valid text file.

import sys
import csv


# =============================================================================
# Read in Validate command line input.
#
#   example:  python dna.py databases/small.csv sequences/5.txt
# =============================================================================

# Check length of command line arguments. Required lenght is 3 (program name,
# filename-csv, filename-txt.)
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt.")


# Check if argument command line arguments 1 is a valid csv, CSV file containing
# the STR counts for a list of individuals.
try:
    with open(sys.argv[1], newline="") as csvfile:
        csvfile_content = csv.reader(csvfile, delimiter=" ", quotechar="|")
        csvfile.close()
except:
    print(f"{sys.argv[1]} does not exist or is not a valid .csv")


# Check if argument command line arguments 1 is a valid .txt, name of a text
# file containing the DNA sequence to identify.
try:
    with open(sys.argv[2]) as txtfile:
        txtfile_content = txtfile.readlines()
        txtfile.close()
except:
    print(f"{sys.argv[2]} does not exist or is not a valid .txt")
