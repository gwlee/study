#https://github.com/TransDecoder/TransDecoder/wiki
#~/hmmer-3.1b1/bin/hmmscan --cpu 8 --domtblout pfam.domtblout Pfam-A.hmm Trinity.fasta.transdecoder_dir/longest_orfs.pep

import os,sys
from Bio import SeqIO

try:
        inputFasta = sys.argv[1]
        inputHmm = sys.argv[2]
except:
        print 'fasta hmm'
        exit(1)




inputDict = dict()
inputList = list()
for rec in SeqIO.parse(open(inputFasta), format='fasta'):
        name = rec.name
        desc = rec.description.split(' ',1)[-1]
        inputDict[name] = desc
        inputList.append(name)

hmmDict = dict()
tmp = ''
i=0
for rec in open(inputHmm):
        if rec.strip().startswith('#'):
                continue

        while rec.strip().find ('  ') != -1:
                rec = rec.strip().replace('  ',' ')

        recs = rec.split(' ',22)
        targetNm, accession, queryNm, desc =  recs[0],recs[1],recs[3],recs[-1]

        if tmp == '':
                tmp = queryNm
                hmmDict[queryNm] = '{}\t{}\t{}'.format(targetNm,accession,desc)
        elif tmp == queryNm:
                pass

        elif tmp != queryNm:
                tmp = queryNm
                hmmDict[queryNm] = '{}\t{}\t{}'.format(targetNm,accession,desc)


for rec in inputList:
        try:
                print '{}\t{}'.format(rec,hmmDict[rec])
        except:
                print '{}\t-\t-\t-'.format(rec)
