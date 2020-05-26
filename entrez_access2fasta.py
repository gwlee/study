import os
import sys
import urllib.request
from Bio import Entrez, SeqIO

Entrez.email = 'anonymous@anonymous.me'

try:
  inputID = sys.argv[1]
except:
  print ('python entrez_access2fasta.py accessionid')
  exit(1)

outputName = inputID.strip()
out = open('{}.fasta'.format(outputName),'w')
print ('')
convert2gi = Entrez.read(Entrez.esearch(db="nucleotide", term=inputID.strip(), retmode="xml"))
gi = convert2gi['IdList'][0]
handle = Entrez.efetch(db="nucleotide", id="{}".format(gi), rettype="fasta", retmode="text")
for item in handle.readlines():
  out.write('{}\n'.format(item.strip()))
  
out.write('\n')
out.close()
