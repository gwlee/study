#https://github.com/TransDecoder/TransDecoder/wiki
#~/ncbi-blast-2.2.30+/bin/blastp -query Trinity.fasta.transdecoder_dir/longest_orfs.pep -db uniprot_sprot.fasta -max_target_seqs 1 -outfmt 6 -evalue 1e-5 -num_threads 10 > blastp.outfmt6

import os,sys
from Bio import SeqIO

try:
        inputFasta = sys.argv[1]
        inputUniprot = sys.argv[2]
        inputBlastp = sys.argv[3]
except:
        print 'fasta uniport blastpoutput'
        exit(1)



uniprotDict = dict()
for rec in SeqIO.parse(open(inputUniprot), format='fasta'):
        name = rec.name
        desc = rec.description.split(' ',1)[-1]
        uniprotDict[name] = desc

inputDict = dict()
inputList = list()
for rec in SeqIO.parse(open(inputFasta), format='fasta'):
        name = rec.name
        desc = rec.description.split(' ',1)[-1]
        inputDict[name] = desc
        inputList.append(name)

blastDict = dict()
for rec in open(inputBlastp):
        recs = rec.strip().split('\t')
        blastDict[recs[0]] = recs[1]

for rec in inputList:
        try:
                outfmt = blastDict[rec]
                print '{}\t{}'.format(rec,uniprotDict[outfmt])
        except:
                print '{}\t-'.format(rec)
