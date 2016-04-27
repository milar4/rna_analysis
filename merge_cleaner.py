"""
Parses files and stores the result in a dictionary.

Dictionary keys are PMID and values are arrays.
"""

import csv
import sys
import re
from retrieve_rnacentral_id import get_md5, get_rnacentral_id


def is_pmid_valid(pmid):
    """
    Valid PMID are numbers.

    Returns True/False
    """
    if re.match("^\d+$", pmid):
        return True
    else:
        return False


def is_sequence_valid(sequence):
    """
    Valid sequence are ATUCG.

    Returns True/False
    """
    if re.match("^[ATUGCRYMKWSBDHN\s]+$", sequence, flags=re.I):
        return True
    else:
        if sequence != '-' or sequence == '-':
            return False

def clean_sequence(sequence):
    """
    Remove newline characters.

    Returns new string
    """
    if is_sequence_valid(line[3]):
        new_sequence = re.sub (r'\s','', sequence)
        return new_sequence
        
EMPTY = '-'
i = open('database1.csv', 'w')
o = csv.writer(i)
# opens the file and assignes it to the variable my_file
# TODO: pass the path and name of the file through an argument.
for fyle in sys.argv[1:]:
    with open(fyle) as my_csv:
        my_file = csv.reader(my_csv)

    	# reads the first line ands stores it in primera_line
        first_line = my_file.next()
        batch = first_line[0]

    	# reads the second line and discards it

        my_file.next()
    	# reads from third line and assignes it to variable line

        previous_pmid = ""

        for line in my_file:
            comments = ''
            result = ""
        
            if is_pmid_valid(line[1]):
                pmid = line[1]
                previous_pmid = pmid
            else:
                pmid = previous_pmid

            if is_sequence_valid(line[3]):
            	comments = EMPTY
                sequence = clean_sequence(line[3])
                md5 = get_md5(sequence)
                result = get_rnacentral_id(md5)
                if result == '':
                    result = EMPTY
                 
            else:
                sequence = EMPTY
                comments = line[3]
                

            o.writerow ([previous_pmid, line[2], sequence, comments, line[4], line[5], line[6], result, batch])









# TODO: serialize the dictionary
