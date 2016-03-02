"""
Parses files and stores the result in a dictionary.

Dictionary keys are PMID and values are arrays.
"""

import csv
import sys
from retrieve_rnacentral_id import get_md5, get_rnacentral_id


def is_pmid_valid(pmid):
    """
    Valid PMID are numbers.

    Returns True/False
    """
    if pmid == '':
        return False

    for character in pmid:
        # if character is in the list of values
        if character not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return False

    return True


def is_sequence_valid(sequence):
    """
    Valid sequence are ATUCG.

    Returns True/False
    """
    if sequence == '':
        return False

    # TODO: match regular expression instead of the following lines
    for nucleotide in sequence:
        # if character is in the list of values
        if nucleotide not in ('A', 'T', 'U', 'G', 'C', 'R', 'Y', 'M', 'K',
                              'W', 'S', 'B', 'D', 'H', 'V', 'N', ' ', '\n'):

            print 'sequence not valid (' + sequence + ')'
            print '*' + nucleotide + '*'
            return False

    return True


def clean_sequence(sequence):
    """
    Remove newline characters.

    Returns new string
    """
    new_sequence = sequence.replace('\n', '')
    new_sequence = new_sequence.replace(' ', '')
    return new_sequence


# opens the file and assignes it to the variable my_file
# TODO: pass the path and name of the file through an argument.
with open(sys.argv[1]) as my_csv:
    my_file = csv.reader(my_csv)

    # create empty dictionary
    results = {}
    # reads the first two lines and discards them
    my_file.next()
    my_file.next()
    # reads from third line and assignes it to variable line
    previous_pmid = ""
    for line in my_file:
        # check key is valid, if not use previous key
        # if is calling a function which returns True or False
        if is_pmid_valid(line[1]):
            pmid = line[1]
            previous_pmid = pmid
        else:
            pmid = previous_pmid

        if is_sequence_valid(line[3]):
            sequence = clean_sequence(line[3])
            md5 = get_md5(sequence)
            result = get_rnacentral_id(md5)
            print result
            if pmid in results:
                results[pmid].append(sequence)
            else:
                results[pmid] = [sequence]
    print results

# TODO: serialize the dictionary
