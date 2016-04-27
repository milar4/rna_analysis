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
        print pmid
        return False


def is_sequence_valid(sequence):
    """
    Valid sequence are ATUCG.

    Returns True/False
    """
    if re.match("^[ATUGCRYMKWSBDHN\s]+$", sequence, flags=re.I):
        return True
    else:
        if sequence != '-':
            print sequence
            return False

def clean_sequence(sequence):
    """
    Remove newline characters.

    Returns new string
    """
    if is_sequence_valid(line[3]):
        new_sequence = re.sub (r'\s','', sequence)
        return new_sequence

# opens the file and assignes it to the variable my_file
# TODO: pass the path and name of the file through an argument.
total_number_of_papers = 0
total_RNA_sequences = 0
total_RNAcentral_IDs = 0
for fyle in sys.argv[1:]:
    with open(fyle) as my_csv:
        my_file = csv.reader(my_csv)
    # create empty dictionary
        results = {}
        id_central = {}
    # reads the first two lines and discards them
        my_file.next()
        my_file.next()
    # reads from third line and assignes it to variable line
        previous_pmid = ""
        total = 0
        have_rna_central_ID = 0
        papers = 0
        for line in my_file:
        # check key is valid, if not use previous key
        # if is calling a function which returns True or False
            if is_pmid_valid(line[1]):
                pmid = line[1]
                previous_pmid = pmid
                papers = papers + 1
            else:
                pmid = previous_pmid
            if is_sequence_valid(line[3]):
                sequence = clean_sequence(line[3])
                total = total + 1
                md5 = get_md5(sequence)
                result = get_rnacentral_id(md5)
                print result
                if pmid in results:
                    results[pmid].append(sequence)
                else:
                    results[pmid] = [sequence]
                if result !='':
                    if pmid in id_central:
                        id_central[pmid].append(result)
                    else:
                        id_central[pmid] = [result]
                    have_rna_central_ID = have_rna_central_ID + 1

    percentage_in_RNAcentral = float(have_rna_central_ID) / total * 100
    print results
    print id_central
    print " In %d papers we found %d RNA sequences" %(papers, total)
    print " %d have RNA central ID" % have_rna_central_ID
    print " %f pencent have RNA central ID" % percentage_in_RNAcentral
    total_number_of_papers = total_number_of_papers + papers
    total_RNA_sequences = total_RNA_sequences + total
    total_RNAcentral_IDs = total_RNAcentral_IDs + have_rna_central_ID
    total_percentage_in_RNAcentral = float(total_RNAcentral_IDs) / total_RNA_sequences * 100
print " TOTAL RESULTS: In %d papers we found %d sequences" %(total_number_of_papers, total_RNA_sequences)
print " %d have RNA central ID (%f percent)" %(total_RNAcentral_IDs, total_percentage_in_RNAcentral)




# TODO: serialize the dictionary
