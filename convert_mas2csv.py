import os
import sys
import re
import operator
from Bio import SeqIO

inSeq = 'msa_2020-04-25.fasta'

dataList=list()

for rec in SeqIO.parse(inSeq,'fasta'):
  desc = rec.description
  seq = str(rec.seq).strip()
  
  tag,subregion,temp,sampleid,otherdesc = '-','-','-','-','-'
  tmp = list()
  items = desc.strip().split('/')
  
  if len(items) == 3:
    tag,subregion,otherdesc = items
    dyear,epi_id,cdate,region = otherdesc.strip().split('|')
    tmp.append(region)
    tmp.append(subregion)
    tmp.append(sampleid)
    tmp.append(epi_id)
    tmp.append(cdate)
    
    for t in list(seq.strip()):
      tmp.append(t)
      
  elif len(items) == 4:
    tag,subregion,otherdesc = items
    dyear,epi_id,cdate,region = otherdesc.strip().split('|')
    tmp.append(region)
    tmp.append(subregion)
    tmp.append(sampleid)
    tmp.append(epi_id)
    tmp.append(cdate)
    
    for t in list(seq.strip()):
      tmp.append(t)
      
  else:
    tag, subregion,tmp1,sampleid,otherdesc = items
    dyear,epi_id,cdate,region = otherdesc.strip().split('|')
    t=seq.strip().split()
    tmp.append(region)
    tmp.append(subregion)
    tmp.append(sampleid)
    tmp.append(epi_id)
    tmp.append(cdate)
    
    for t in list(seq.strip()):
      tmp.append(t)
      
  dataList.append(tmp)

s=sorted(dataList,key=operator.itemgetter(0,1,2,4))

ow = open('output.csv','w')
for x in list(map(list,zip(*s))):
  ow.write(('{}\n'.format('\t'.join(x))))
ow.close()
