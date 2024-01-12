import argparse
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse
import math 



parser = argparse.ArgumentParser()
#parser.add_argument('-v', '--VCF', required=True, type=str,help='path to VCF to be processed')
parser.add_argument('-d', '--working_directory', required=True, type=str, help='directory for all outputs (make sure this directory will have enough space!!!!)')
parser.add_argument('-of', '--outfile', required=True, type=str, help='name for output file-omit suffix (make sure this directory will have enough space!!!!)')
parser.add_argument('-r', '--ref_file', required=True, type=str, help="path to reference fasta file")
parser.add_argument('-vir', '--viridian_mutations', required=True, type=str, help="path to mutation file for mat1")
parser.add_argument('-gb', '--genbank_mutations', required=True, type=str, help="path to mutation file for mat2")
parser.add_argument('-rm', '--remove_files', required=False, default=False, type=bool, help="if True, remove all mutation files created for analysis, (mutation files created in mat directory)")

#parser.add_argument('-l', '--logging', required=False, default=True, type=bool, help="if True, logging.debug verbose logging to diff.log, else suppress most logging")

args = parser.parse_args()
dir = args.working_directory
if not dir.endswith('/'):
     dir = dir+'/'
ref = args.ref_file
m1 = args.viridian_mutations
m2 = args.genbank_mutations
of = args.outfile
#m1name = pb[:-3]
m1name = m1.split('/')[-1][:-4]
m2name = m2.split('/')[-1][:-4]
print(m1name)
print(m2name)



    
#treedir = '/'.join(tree.split('/')[:-1])
#print('treedir', treedir)
#keep software as unit
software_dir = '/'.join(sys.argv[0].split('/')[:-1])+'/'
#print(software_dir)
#rm = args.remove_files

#os.system(f'matUtils summary -i {pb} -m {tree}.muts.tsv')

#make backmut1
os.system(f'python3 {software_dir}back-mutation.py -f {ref} -m {m1} -o {dir} -n {m1name}')
#make backmut2
os.system(f'python3 {software_dir}back-mutation.py -f {ref} -m {m2} -o {dir} -n {m2name}')


#if rm:
#    os.system(f'rm {tree}.muts.tsv')
#    os.system(f'rm {tree}.mutstat.txt')

#can combine mult trees
'''
histo = {}
for f in os.listdir(dir):
	if f.startswith('backmuts-artic'):
		print(f)
		with open(f) as f:
			line=f.readline()
			for line in f:
				line = line.strip().split()
				print(line)
					
				if line[0] not in histo:
					histo[line[0]] = int(line[3])
				else:
					histo[line[0]] += int(line[3]
                    '''


#for single tree, does not combine more than one tree
def make_histo(mutname):
    histo = {}
    with open(f'{dir}/backmuts-{mutname}') as f:
        line=f.readline()
        for line in f:
            line = line.strip().split()
            #print(line)
                
            if int(line[0]) not in histo:
                histo[int(line[0])] = int(line[3])
            else:
                histo[int(line[0])] += int(line[3])
    print(histo)
           
    #mx = sorted(list(histo.keys()))
    #print(histo.values())
    #my = [histo[x] for x in mx]


    #print(mx)
    #print(my)
    #list of tuples containing position and count, caused binning errors do not use
    
    '''
    #counts for all positions
    pos = []
    #count = []				
    for h in histo:
        pos.append((int(h),int(histo[h])))
        #count.append(int(histo[h]))
    print(len(pos))
    '''

    #works well for binning, less efficient
    '''
    pos_list = []
    for h in histo:
        pos_list.extend([int(h)]*int(histo[h]))
    '''
    #print(histo[15521])
    counts = []          
    for i in range(1, len(ref_seq)+1):
        if i not in histo:
            counts.append(0)
        else:
            counts.append(histo[i])
            if histo[i] > 6000:
                print(histo[i])

    #print(counts)
    return sorted(counts, reverse = True)
    #return mx, my



    
ref_seq = ''
with open(ref) as r:
	for line in r:
		if not line.startswith('>'):
			line = line.strip()
			ref_seq += line


#contains all positions and their counts including counts of 0
'''
pos2 = []          
for i in range(1, len(ref_seq)+1):
    if i not in histo:
        pos2.append((i, 0))
    else:
        pos2.append((i, histo[i]))

print('pos2',len(pos2))
'''


#write counts to file     
'''
with open(f'{dir}{of}-cpb.txt', 'w') as ow:
    for p in pos:
        ow.write(f'{p[0]}\t{p[1]}\n')
        '''
         
#m1x, m1y = make_histo(m1name)
#m2x, m2y = make_histo(m2name)   

counts1 = make_histo(m1name)
counts2 = make_histo(m2name) 
print(counts2)

c1_list = []
c2_list = []
xs = []
for i in range(10000):
    xs.append(i)
    c1c = 0
    for j in range(len(counts1)):
        if counts1[j] > i:
            c1c +=1
        else: 
            c1_list.append(c1c)
            break

    c2c = 0
    for j in range(len(counts2)):
        if counts2[j] > i:
            c2c +=1
        else: 
            c2_list.append(c2c)
            break

print(c2_list)

'''
c1 = sorted(counts1, reverse=True)
c2 = sorted(counts2, reverse=True)
#print(c1[0:100])
#print(c2[0:100])

xq = [i for i in range(len(c1)+1)]
#print(xq)
print(sum(c1))
print(sum(c2))

totals1 = [0] 
current = 0
for i in range(len(c1)):
    current += c1[i]
    if current == 0:
        print('done',i)
    totals1.append(current)

totals2 = [0] 
current = 0
for i in range(len(c1)):
    current += c2[i]
    if current == 0:
        print(i)
    totals2.append(current)

#tots1 = [0] 
current = sum(c1)
tots1 = [current]
x1 = [0]
for i in range(len(c1)):
    current -= c1[i]

    if current == 0:
        print('done',i)
        break
    tots1.append(current)
    x1.append(i+1)

#tots2 = [0] 
current = sum(c2)
tots2 = [current] 
x2 = [0]
for i in range(len(c1)):
    current -= c2[i]
    if current == 0:
        print('done',i)
        break
    tots2.append(current)
    x2.append(i+1)

#print(tots1)
#print(len())
'''
'''
assert len(counts1) == len(counts2)
outs = []
#outsGB = []
for pos in range(len(counts1)):
    #if counts1[pos]>=1000 or counts2[pos]>=1000:
    if counts1[pos] > counts2[pos]*3 or counts2[pos] > counts1[pos]*16:
        if counts1[pos]>=100 or counts2[pos]>=100:
            outs.append((pos, counts1[pos], counts2[pos]))
        #if :
        #    outsGB.append((pos, counts1[pos], counts2[pos]))
            #print(counts1[pos], counts2[pos])

#print(outs)
#set(outs)
#print(len(outs))
'''


        
figureHeight=6
figureWidth=6

panel1Width=5
panel1Height=5

panel2Width=6.0
panel2Height=2.0

#panel3Width=6.0
#panel3Height=1.9

#panel4Width=6.0
#panel4Height=1.9

relativePanel1Width=panel1Width/figureWidth
relativePanel1Height=panel1Height/figureHeight

relativePanel2Width=panel2Width/figureWidth
relativePanel2Height=panel2Height/figureHeight

#relativePanel3Width=panel3Width/figureWidth
#relativePanel3Height=panel3Height/figureHeight

#relativePanel4Width=panel4Width/figureWidth
#relativePanel4Height=panel4Height/figureHeight
# left,bottom, width,height

#panel1=plt.axes([0.11,0.11,relativePanel1Width,relativePanel1Height])
panel1=plt.axes([0.1,0.1,relativePanel1Width,relativePanel1Height])


#panel1.set_aspect('equal')
#panel2=plt.axes([0.58,0.11,relativePanel2Width,relativePanel2Height])
#panel2=plt.axes([0.61,0.17,relativePanel2Width,relativePanel2Height])

#panel3=plt.axes([0.11,0.59,relativePanel3Width,relativePanel3Height])
#panel3=plt.axes([0.11,0.58,relativePanel3Width,relativePanel3Height])

#panel4=plt.axes([0.58,0.58,relativePanel4Width,relativePanel4Height])
#panel1.tick_params(bottom=True, labelbottom=True,
#                   left=True, labelleft=True,
#                   right=False, labelright=False,
#                   top=False, labeltop=False)

#panel2.tick_params(bottom=True, labelbottom=True,
#                   left=True, labelleft=True,
#                   right=False, labelright=False,
#                   top=False, labeltop=False)

#panel1.set_ylabel('Number of Reversions Removed')
panel1.set_ylabel('Number of Genomic Positions Above Reversion Threshold')
panel1.set_xlabel('Reversion Threshold')


panel1.set_title('Genomic Positions Above a Certain Threshold of Reversions')
#panel2.set_xlabel('Number of Sites Masked')

#panel2.set_xlabel('x Distance From y=x Line')
#panel3.set_ylabel('y Distance From y=x Line')
#panel2.set_xlabel('Jaccard Indices')

#panel1.set_title(f'Reversions in Intersection Tree')
#if using dictionaries 

'''
xlist1 = []
for gene in range(len(data1)):
    xlist1.append(data1[gene])

xlist2 = []
for gene in data2:
    xlist2.append(data2[gene])
'''

'''
bins = np.arange(0,len(ref_seq)+1,100)
file1hist,bins = np.histogram(m1hist,bins)
file2hist,bins = np.histogram(m2hist, bins)

#print(len(file1hist))
#print(len(file2hist))
#print(bins)
#file2hist,bins=np.histogram(file2,bins)


maxHeight = 0
panel1.scatter()

for index in range(0,len(file1hist),1):
    bottom=0
    left=bins[index]
    width=bins[index+1]-left
    height1=file1hist[index]
    #if height != 0:
    #    print('bin', left)
    #    print('height',height)
    if height1 > maxHeight: 
        maxHeight = height
    #
    rectangle1=mplpatches.Rectangle([left,bottom],width,height,
                                 linewidth=0.1,
                                 edgecolor='black',
                                 facecolor=(.5,.5,.5)
    )
    panel1.add_patch(rectangle1)

#panel1.set_ylim(0,maxHeight+1)
#panel1.set_yscale("log")
'''



#no second panel 
'''
maxHeight = 0
for index in range(0,len(file2hist),1):
    bottom=0
    left=bins[index]
    width=bins[index+1]-left
    height=file2hist[index]
    if height > maxHeight: 
        maxHeight = height
    rectangle1=mplpatches.Rectangle([left,bottom],width,height,
                                 linewidth=0.1,
                                 edgecolor='black',
                                 facecolor=(.5,.5,.5)
    )
    panel2.add_patch(rectangle1)
panel2.set_ylim(0,maxHeight+20)
ax1.scatter(x[:4], y[:4], s=10, c='b', marker="s", label='first')
'''

#to color code, you will need to iterate through all positions and graph points one by one 
'''
panel1.plot(xq, totals1, c='b', label='second', alpha=.5)
panel1.plot(xq, totals2, c='r', label='second', alpha=.5)
panel2.set_xlim(0,100)
panel2.plot(xq, totals1, c='b', label='second', alpha=.5)
panel2.plot(xq, totals2, c='r', label='second', alpha=.5)
'''

#panel1.plot(x1, tots1, c='b', label='second', alpha=.5)
#panel1.plot(x2, tots2, c='r', label='second', alpha=.5)
panel1.set_ylim(0,250)
#plt.legend()
#panel2.set_xlim(0,10)
Viridian = panel1.plot(xs,c1_list, c='b', label='Viridian', alpha=.5)
Genbank = panel1.plot(xs, c2_list, c='r', label='Genbank', alpha=.5)
plt.legend()
plt.savefig( f'{dir}{of}.png',dpi=600)
