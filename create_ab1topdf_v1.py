from Bio import SeqIO
import matplotlib.pyplot as plt

record = SeqIO.read(ab1_file_path, 'abi')
seq = record.seq

poc = record.annotations['abif_raw']['PLOC1']
a_seq = record.annotations['abif_raw']['DATA10']
c_seq = record.annotations['abif_raw']['DATA12']
g_seq = record.annotations['abif_raw']['DATA9']
t_seq = record.annotations['abif_raw']['DATA11']

data = {"A":a_seq, "C":c_seq,"G":g_seq,"T":t_seq}

plt.figure(figsize=(len(poc)/10,5))
for base, color in zip("ACGT",["g","b","k","r"]):
    plt.plot(data[base],color=color)

tmp = [None]*len(a_seq)
i=0
for pnt in poc:
    tmp[pnt]=seq[i]
    i+=1
    
plt.xticks(range(len(tmp)),tmp, fontsize=6)
plt.savefig('output.pdf')
