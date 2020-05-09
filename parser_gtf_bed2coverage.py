import os,sys,gzip,operator

try:
        inputgtf = sys.argv[1]
        inputGene = sys.argv[2]
        inputbed = sys.argv[3]
except:
        print 'inputgtf.gz inputGene inputbed'
        exit(1)

'''
inputgtf (gtf)
chr1    refGene transcript      11869   14362   .       +       .       gene_id "LOC102725121"; transcript_id "NR_148357";  gene_name "LOC102725121";
chr1    refGene exon    11869   12227   .       +       .       gene_id "LOC102725121"; transcript_id "NR_148357"; exon_number "1"; exon_id "NR_148357.1"; gene_name "LOC102725121";
chr1    refGene exon    12613   12721   .       +       .       gene_id "LOC102725121"; transcript_id "NR_148357"; exon_number "2"; exon_id "NR_148357.2"; gene_name "LOC102725121";
chr1    refGene exon    13221   14362   .       +       .       gene_id "LOC102725121"; transcript_id "NR_148357"; exon_number "3"; exon_id "NR_148357.3"; gene_name "LOC102725121";

bedtools sort -i in.bed > in.sort.bed
bedtools merge -i in.sort.bed > in.merge.bed
inputbed (aka in.merge.bed)
chr1    12080   12251   ref|DDX11L1,ref|NR_046018
chr1    12595   12802   ref|DDX11L1,ref|NR_046018
'''

gtfList = list()
geneList = list()
transList = list()
for rec in gzip.open(inputgtf,'rb'):
        rChr,rSource,rType,rStart,rEnd,rTmp,rStrand,rBase,rDesc = rec.strip().split('\t')

        geneName = ''
        transcriptName = ''
        exonNum = ''
        for item in rDesc.strip().split('; '):
                if item.startswith('gene_name'):
                        geneName = item.strip().split(' ')[-1][1:-2]
                        continue

                if item.startswith('transcript_id'):
                        transcriptName = item.strip().split(' ')[-1][1:-1]
                        continue

                if item.startswith('exon_number'):
                        exonNum = item.strip().split(' ')[-1][1:-1]
                        continue

                else:
                        pass

        if inputGene == geneName:
                if rType == 'exon':
                        transList.append(transcriptName)
                        geneList.append((geneName,transcriptName))
                        gtfList.append((rChr,rStart,rEnd,geneName,transcriptName,exonNum))
                        #print '{}\t{}\t{}\t{}|{}|{}'.format(rChr,rStart,rEnd,geneName,transcriptName,exonNum)

geneList = list(set(geneList))
transList = list(set(transList))

bedList = list()
for rec in open(inputbed):
        rChr,rStart,rEnd,rDesc = rec.strip().split('\t')
        for tmp in rDesc.strip().split(','):
                try:
                        src,src_value = tmp.strip().split('|')
                        if src_value.strip() == inputGene.strip() :
                                bedList.append((rChr,int(rStart),int(rEnd)))
                                break
                except:
                        pass

if len(bedList) == 0:
        for rec in open(inputbed):
                rChr,rStart,rEnd,rDesc = rec.strip().split('\t')
                for tmp in rDesc.strip().split(','):
                        try:
                                src,trans = tmp.strip().split('|')
                                if trans in transList:
                                        bedList.append((rChr,int(rStart),int(rEnd)))
                                        break

                        except:
                                pass

else:
        pass

bedList = sorted(bedList, key = operator.itemgetter(1, 2))


for rec in geneList:
        rGene,rTrans = rec
        tmp = list()
        transPos = list()
        gtfLenList = list()
        for item in gtfList:
                iChr,iStart,iEnd,iGene,iTrans,iExon = item
                if iGene == rGene:
                        if iTrans == rTrans:
                                tmp.append((iChr,int(iStart),int(iEnd)))
                                gtfLenList.append(int(iEnd)-int(iStart))
                                transPos.append(int(iStart))
                                transPos.append(int(iEnd))

        tLenList = list()
        transLen = list()
        bedLenList = list()

        for item in tmp:
                iChr,iStart,iEnd = item

                for bPos in bedList:
                        bChr,bStart,bEnd = bPos
                        if iStart < bStart and bEnd < iEnd:
                                        bedLenList.append(bEnd-bStart)
                                        continue

                        if bStart < iStart and iEnd < bEnd:
                                        bedLenList.append(iEnd-iStart)
                                        continue

                        if iStart == bStart and bEnd == iEnd:
                                        bedLenList.append(bEnd-bStart)
                                        continue

                        if iStart < bStart < iEnd and iEnd < bEnd:
                                        bedLenList.append(iEnd-bStart)
                                        continue

                        if iStart < bEnd < iEnd and bStart < iStart:
                                        bedLenList.append(bEnd-iStart)
                                        continue

                        if iStart == bStart and iEnd < bEnd:
                                        bedLenList.append(iEnd-iStart)
                                        continue

                        if iStart == bStart and bEnd < iEnd:
                                        bedLenList.append(bEnd-bStart)
                                        continue

                        if iEnd == bEnd and iStart < bStart:
                                        bedLenList.append(bEnd-bStart)
                                        continue

                        if iEnd == bEnd and bStart < iStart:
                                        bedLenList.append(iEnd-iStart)
                                        continue

        transPos.sort()
        print '{}\t{}\t{}\t{}\t{}\t{}'.format(rGene,rTrans,transPos[0],transPos[-1],sum(gtfLenList),sum(bedLenList))

