"""
Copyright [2009-2014] EMBL-European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

An example Python script showing how to retrieve the RNAcentral id for an RNA sequence.

Usage:
python retrieve_rnacentral_id.py
"""

import hashlib
import requests # pip install requests


def get_md5(sequence):
	"""
	Calculate md5 for an RNA sequence
	"""
	# RNAcentral stores DNA md5 hashes
	sequence = sequence.replace('U','T')
	# get the md5 digest
	m = hashlib.md5()
	m.update(sequence)
	return m.hexdigest()

# get the RNAcentral id
def get_rnacentral_id(md5):
	"""
	Parse json output and return the RNAcentral id.
	"""
	url = 'http://rnacentral.org/api/v1/rna'
	r = requests.get(url, params = {'md5': md5})
	data = r.json()
	if data['count'] > 0:
		return data['results'][0]['rnacentral_id']
	else:
		return 'RNAcentral id not found'

# This sequence has an RNAcentral id
sequence = 'CUGAAUAAAUAAGGUAUCUUAUAUCUUUUAAUUAACAGUUAAACGCUUCCAUAAAGCUUUUAUCCA'
md5 = get_md5(sequence)
print get_rnacentral_id(md5)  # URS00002C9E9D

# This sequence doesn't have an RNAcentral id
sequence = 'Not an RNA sequence'
md5 = get_md5(sequence)
print get_rnacentral_id(md5) # RNAcentral id not found
