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
#   2.  * Your program should open the CSV file and read its contents into
#       memory.
#       * You may assume that the first row of the CSV file will be the column
#       names. The first column will be the word name and the remaining columns
#       will be the STR sequences themselves.
#   3.  * Your program should open the DNA sequence and read its contents into
#       memory.
#   4.  * For each of the STRs (from the first line of the CSV file), your
#       program should compute the longest run of consecutive repeats of the
#       STR in the DNA sequence to identify.


# clear && mypy dna.py && black dna.py && python dna.py databases/small.csv sequences/5.txt


import sys
import csv
from typing import Dict, List
from itertools import zip_longest


# =============================================================================
# Validate command line input and read into memory
#
# =============================================================================

# Check length of command line arguments. Required lenght is 3 (program name,
# filename-csv, filename-txt.)
if len(sys.argv) != 3:

    print("Usage: python dna.py data.csv sequence.txt.")


# Check if argument command line arguments 1 is a valid csv, CSV file containing
# the STR counts for a list of individuals.
try:

    with open(sys.argv[1], newline="") as csvfile:

        csvfile_content = csv.reader(csvfile, delimiter=",", quotechar="|")
        rows_csv = [row for row in csvfile_content]
        csvfile.close()

except:

    print(f"{sys.argv[1]} does not exist or is not a valid .csv")


# Check if argument command line arguments 1 is a valid .txt, name of a text
# file containing the DNA sequence to identify.
try:

    with open(sys.argv[2]) as txtfile:

        txtfile_content = txtfile.readlines()
        rows_txt = [row for row in txtfile_content]
        txtfile.close()

except:

    print(f"{sys.argv[2]} does not exist or is not a valid .txt")


# =============================================================================
# Read .csv and .txt content into memeory
#
#   CSV Conente as "organisms"
#   * First row: colum names.
#   * First colum: word name
#   * Remaining colms: STR sequnces.
#
#   DNA sqeunece as "dna_str"
# =============================================================================


# Get column names: names, STR_0, STR_1, ..., STR_n
organisms_column_names: list = rows_csv[0]

# Get organims: key: name, value: STC count
organisms: Dict[str, List[str]] = {}
for row in rows_csv[1:]:

    name: str = row[0]
    organisms[name] = row[1:]

# DNA as string
dna_str: str = rows_txt[0]


# =============================================================================
# Compute the longest run of consecutive repeats each STR in
# organisms_column_names.
# ============================================================================

strs_longest_run_consecutive_repeats: Dict[str, int] = {}


# 1st elemnt in organisms_column_names is "name" so no STR.
# for str_word in organisms_column_names[1:]:
#
#    x = []
#    for count, _ in enumerate(dna_str):
#        if dna_str[count:count+4] == str_word:
# lst = []
# for count, _ in enumerate(dna_str):
#    if dna_str[count : count + 4] == "AATG":
#        lst.append(True)
#    else:
#        lst.append(False)
#
# longest_run = 0
# for i in lst:
#    current_run = 0
#    if i = True:


str_of_interest = "AAAA"

for count_0, _ in enumerate(dna_str):

    # Find next occurence of STR of interest
    if dna_str[count_0:count_0+4]:
        consecutive_current = 1
        pass


# i = 0
# max_count = 0
# print(f"DNA: {dna_str}")
# for c0, _ in enumerate(dna_str):
#     # Find an occurence of AAAA
#     if dna_str[c0 : c0 + 4] == "AAAA":
#
#         # consecutive repeats; 1 as we found a "STR"
#         current_count = 1
#
#         # Make a copy of the rest of the string after STR
#         rest_of_string = dna_str[c0 + 4 :]
#         print(rest_of_string)
#
#         # Check if the next four chars are also the same STR.
#         # If yes, increase current counter and cut string (vie reassignment)
#         if rest_of_string[0:4] == "AAAA":
#             current_count += 1
#             rest_of_string = rest_of_string[4:]
#         else:
#             max_count = current_count if current_count > max_count else max_count
#             break))
