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
parser.add_argument('-vir', '--viridian_mutations', required=True, type=str, help="path to mutation file for viridian MAT")
parser.add_argument('-gb', '--genbank_mutations', required=True, type=str, help="path to mutation file for genbank MAT")
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

m1name = m1.split('/')[-1][:-4]
m2name = m2.split('/')[-1][:-4]
print(m1name)
print(m2name)


    
#treedir = '/'.join(tree.split('/')[:-1])
#print('treedir', treedir)
#keep software as unit
software_dir = '/'.join(sys.argv[0].split('/')[:-1])+'/'
if software_dir == '/':
	software_dir = './'
#print(software_dir)
rm = args.remove_files

#old code, can accept pb instead of mutation file and produce mutation file with code 
#removed bc assumes usher is installed and included in environment path
#
#os.system(f'matUtils summary -i {pb} -m {tree}.muts.tsv')

#make backmut1
os.system(f'python3 {software_dir}back-mutation.py -f {ref} -m {m1} -o {dir} -n {m1name}')
#make backmut2
os.system(f'python3 {software_dir}back-mutation.py -f {ref} -m {m2} -o {dir} -n {m2name}')

#for single tree
def make_histo(mutname):
    '''
    makes histogram of 
    '''
    histo = {}
    with open(f'{dir}backmuts-{mutname}') as f:
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
    
    counts = []          
    for i in range(1, len(ref_seq)+1):
        if i not in histo:
            counts.append(0)
        else:
            counts.append(histo[i])

    print('pos2',counts)
    return counts
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

assert len(counts1) == len(counts2)
print(len(counts1))
#outsGB = []
sortedc1 = sorted(counts1)
sortedc2 = sorted(counts2)
outsc1 = sortedc1[-3:]
outsc2 = sortedc2[-3:]
print(sortedc1)
print('outssc1',outsc1)
print('outssc2', outsc2)

outs = []
for c in outsc1:
    print(c)
    ind = counts1.index(c)
    print('ind', ind)
    print(counts2[ind])
    outs.append((c,counts2[ind],ind))

for c in outsc2:
    ind = counts2.index(c)
    print('ind', ind)
    print(counts1[ind])
    outs.append((counts1[ind],c,ind))


outs_zoom = []
sc1_zoom = [i for i in counts1 if i>100 and i < 5000 and counts2[counts1.index(i)] < 5000 and counts2[counts1.index(i)] > 100]
sc2_zoom = [i for i in counts2 if i>100 and i < 5000 and counts1[counts2.index(i)] < 5000 and counts1[counts2.index(i)] > 100]
print(sc2_zoom)
outsc1_zoom = sorted(sc1_zoom)[-3:]
outsc2_zoom = sorted(sc2_zoom)[-3:]
for c in outsc1_zoom:
    print(c)
    ind = counts1.index(c)
    print('ind', ind)
    print(counts2[ind])
    outs_zoom.append((c,counts2[ind],ind))

for c in outsc2_zoom:
    ind = counts2.index(c)
    print('ind', ind)
    print(counts1[ind])
    outs_zoom.append((counts1[ind],c,ind))

        

figureHeight=5
figureWidth=10


panel1Width=6.0
panel1Height=2

panel2Width=6.0
panel2Height=2.0

panel3Width=6
panel3Height=1.9

panel4Width=6.0
panel4Height=2

relativePanelWidth=panel1Width/figureWidth
#relativePanel1Height=panel1Height/figureHeight
relativePanelHeight=relativePanelWidth
print(figureHeight)
print(relativePanelWidth)

fig, axs = plt.subplots(nrows = 1, ncols= 2, figsize = (8,4),layout="constrained")
print(fig)
print(axs)
panel1 = axs[0]
panel2 = axs[1]
#relativePanel2Width=panel2Width/figureWidth
#relativePanel2Height=panel2Height/figureHeight
#relativePanel2Height=relativePanel2Width

#relativePanel3Width=panel3Width/figureWidth
#relativePanel3Height=panel3Height/figureHeight

#relativePanel4Width=panel4Width/figureWidth
#relativePanel4Height=panel4Height/figureHeight
# left,bottom, width,height

#panel1=plt.axes([0.11,0.11,relativePanel1Width,relativePanel1Height])
#panel2=plt.axes([0.11,0.11,relativePanelWidth,relativePanelWidth])

#makes plots square?
panel2.set_aspect('equal')

#panel1=plt.axes([0.6,0.11,relativePanelWidth,relativePanelWidth])
panel1.set_aspect('equal')
#panel2=plt.axes([0.58,0.11,relativePanel2Width,relativePanel2Height])

#panel3=plt.axes([0.11,0.59,relativePanel3Width,relativePanel3Height])
#panel3=plt.axes([0.12,0.58,relativePanel3Width,relativePanel3Height])

#panel4=plt.axes([0.58,0.58,relativePanel4Width,relativePanel4Height])
#panel1.tick_params(bottom=True, labelbottom=True,
#                   left=True, labelleft=True,
#                   right=False, labelright=False,
#                   top=False, labeltop=False)

#panel2.tick_params(bottom=True, labelbottom=True,
#                   left=True, labelleft=True,
#                   right=False, labelright=False,
#                   top=False, labeltop=False)

panel1.set_xlabel('Reversion Counts in Viridian')
panel1.set_ylabel('Reversion Counts in GB')
#panel2.set_xlabel('Jaccard Indices')

#panel1.set_title(f'Reversions in Intersection Tree')
#panel2.set_title(f'{input2}')

#panel2.set_xlabel('x Distance From y=x Line')
#panel3.set_ylabel('y Distance From y=x Line')
#panel2.set_xlabel('Jaccard Indices')

#panel1.set_title(f'Reversions in Intersection Tree')
#if using dictionaries 

panel2.set_xlabel('Reversion Counts in Viridian')
panel2.set_ylabel('Reversion Counts in GB')
#panel2.set_xlabel('Jaccard Indices')

#panel2.set_title(f'Reversions in Intersection Tree')

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

panel1.scatter(counts1, counts2, s=5, c='b', marker="o", label='second', alpha=.1)

xdists = []
ydists = []
dists = []
udists = [[],[]]
odists = [[],[]]
for c in range(len(counts1)):
    #if counts1[c] != counts2[c]:
    #print(counts1[c], counts2[c])
    x = counts1[c]
    y = counts2[c]
    xdist = x - y
    ydist = y - x
    xdists.append(xdist)
    ydists.append(ydist)
    
    d = abs(x - y)/math.sqrt(2)
    #print('xdist', xdist, 'ydist', ydist, 'dist', d)
    #dists.append(d)
    if x >= y:
        udists[0].append(d)
        udists[1].append(y)
    if x <= y:
        odists[0].append(x)
        odists[1].append(d)
    '''
    if x > y:
        udists.append(d)
    if y > x:
        odists.append(d)
        '''
#print(ydists)

#y_lim = plt.ylim()
#x_lim = plt.xlim()
#panel1.plot(x_lim, y_lim, 'k-', color = 'r')
#panel1.scatter(m2x, m2y, s=2, c='b', marker="s", label='first', alpha = .1)



panel1.axline((0, 0), slope=1, alpha=.7)


#panel1.set_yscale("log")
#panel1.set_xscale("log")
pan1y = (panel1.get_ylim())
pan1x = (panel1.get_xlim())
panel1.set_ylim(panel1.get_xlim())

#scatter plot for under line distance from y=x
#panel2.set_xlabel('x>y points distance from y=x line')
#panel2.scatter(udists[0], udists[1], s=5, c='b', marker="o", label='second', alpha=.1)
#panel2.set_ylim(panel1.get_ylim())
#panel2.set_ylim(panel)
#panel2.set_yscale("log")
#panel2.set_xscale("log")
#panel2.xaxis.set_tick_params(labelsize=7)

#scatter plot for over line distance from y=x
#panel3.set_ylabel('x<y points distance from\ny=x line')
#panel3.scatter(odists[0], odists[1], s=5, c='b', marker="o", label='second', alpha=.1)
#panel3.set_xlim(pan1x)
#panel3.set_yscale("log")
#panel3.set_xscale("log")
#panel2.scatter(counts1, counts2, s=5, c='b', marker="o", label='second', alpha=.1)
#panel2.set_xlim(10,1000)
#panel2.set_ylim(10,1000)

#panel3.yaxis.set_tick_params(labelsize=7)

panel2.scatter(counts1, counts2, s=5, c='b', marker="o", label='second', alpha=.1)
panel2.set_xlim(100,5000)
panel2.set_ylim(100,5000)
panel2.axline((0, 0), slope=1, alpha=.7)
#panel4.set_yscale("log")
#panel4.set_xscale("log")

rectangle1=mplpatches.Rectangle([100,100],790,990,
                                 linewidth=.7,
                                 edgecolor='black', facecolor='none', ls='--')
#cant even see this on linear 
#panel1.add_patch(rectangle1)

'''
plt.annotate('a polar annotation',
            xy=(.4, .4),  # theta, radius
            #xytext=(0.05, 0.05),    # fraction, fraction
            arrowcoords='figure fraction',
            arrowprops=dict(facecolor='black'),
            horizontalalignment='left',
            verticalalignment='bottom')
#arrow = plt.arrow(.45,.45,100,100, color='red')
'''
'''
ax.annotate('point offset from data',
            xy=(3, 1), xycoords='data',
            xytext=(-10, 90), textcoords='offset points',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='center', verticalalignment='bottom')
            '''
#arrow = mplpatches.Arrow(.45,.55, .6, .5)
#plt.axes.Axes.add_patch(arrow)
#panel1.add_patch(p.Rectangle((10,10), 800, 800)
'''
#scatter plot for x distance from y=x
panel2.set_xlabel('x Distance From y=x Line')
panel2.scatter(xdists, counts2, s=5, c='b', marker="o", label='second', alpha=.1)
panel2.set_yscale("log")
panel2.set_xscale("symlog")
panel2.xaxis.set_tick_params(labelsize=7)

#scatter plot for y distance from y=x
panel3.set_ylabel('y Distance From y=x Line')
panel3.scatter(counts1, ydists, s=5, c='b', marker="o", label='second', alpha=.1)
panel3.set_yscale("symlog")
panel3.set_xscale("log")
panel3.yaxis.set_tick_params(labelsize=7)
'''


#print(panel2.get_xticklabels())
#xticklabels = list(map(str, panel2.get_xticklabels()))
#xlab = ['-10^{4}','-10^{3}','-10^{2}','-10^{1}','0', '10^{1}','10^{2}','10^{3}','10^{4}']
#panel2.set_xticks(rotation='vertical')

'''
jitter_x = (np.random.rand() - 0.5) * jitter_amount
        jitter_y = (np.random.rand() - 0.5) * jitter_amount
        ax.annotate(
            f'{label}',
            xy=(x_coord, y_coord),
            xytext=(jitter_x, jitter_y),
            textcoords='offset points', ha='right', va='bottom',
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )
'''




# Add the arrow patch to the axis

'''
# Annotate the point
arrow_length = 1
arrow_head_width = 1
for o in outs:
    arrow = mplpatches.FancyArrowPatch((o[0], o[1]), (o[0] + arrow_length, o[1]),
                            arrowstyle='->', mutation_scale=10, color='black', linewidth=1)
    panel1.add_patch(arrow)
    '''

# Set arrow properties
arrow_length = 3000
#arrow_width = 0.01  # Adjust the width for the arrowhead
label_offset = 500
#outs.append((27001,27001,5))
# Create arrows pointing to each coordinate in outs
for o in outs:
    
    
        
    arrow_end = (o[0], o[1] + label_offset)
    arrow_start = (o[0], o[1]+ arrow_length + label_offset)
    if o[2] == 240:
        arrow_end = (o[0] , o[1] )
        arrow_start = (o[0] + 1200, o[1]+ arrow_length)
    if o[2] == 15520:
        arrow_end = (o[0], o[1] + label_offset)
        arrow_start = (o[0] - 1200, o[1]+ arrow_length + label_offset)
    if o[2] == 23947:
        arrow_end = (o[0], o[1] + label_offset)
        arrow_start = (o[0] + 1200, o[1]+ arrow_length + label_offset)
    
    arrow = mplpatches.FancyArrowPatch(arrow_start, arrow_end,
                            arrowstyle='->', mutation_scale=7, color='black', linewidth=1)
    panel1.add_patch(arrow)
    
    # Add labels
    panel1.text(arrow_start[0], arrow_start[1] , f'{o[2]}', ha='center', va='bottom', fontsize=9)

arrow_length = 500
#arrow_width = 0.01  # Adjust the width for the arrowhead
label_offset = 50
np.random.seed(5)
for o in outs_zoom:
    
    jitter_x = (np.random.rand())*700
    jitter_y = (np.random.rand())* 300
    #print(jitter_x)
    #print(jitter_y)
    #arrow_end = (o[0], o[1] + label_offset)
    #arrow_start = (o[0] + jitter_x, o[1]+ arrow_length + jitter_y + label_offset)
    arrow_end = (o[0], o[1] + label_offset)
    arrow_start = (o[0], o[1]+ arrow_length + label_offset)
    if o[2] == 240:
        arrow_end = (o[0], o[1] + label_offset)
        arrow_start = (o[0] + 150, o[1]+ arrow_length + label_offset - 75)
    if o[2] == 22812:
        arrow_end = (o[0], o[1] + label_offset)
        arrow_start = (o[0] + 350, o[1]+ arrow_length + 200 + label_offset)
    if o[2] == 24409:
        arrow_end = (o[0], o[1] + label_offset)
        arrow_start = (o[0] + 900, o[1]+ arrow_length + 600 + label_offset)   
    if o[2] == 27637:
        arrow_end = (o[0], o[1] + label_offset)
        arrow_start = (o[0] + 500, o[1]+ arrow_length + 0 + label_offset)
        
    
    arrow = mplpatches.FancyArrowPatch(arrow_start, arrow_end,
                            arrowstyle='->', mutation_scale=7, color='black', linewidth=1)
    panel2.add_patch(arrow)
    
    # Add labels
    #if o[2] == 27637:
    #    panel4.text(o[0] + jitter_x, o[1] + arrow_length +label_offset + jitter_y, f'{o[2]}', ha='center', va='bottom', fontsize=9)

    
    panel2.text(arrow_start[0], arrow_start[1], f'{o[2]}', ha='center', va='bottom', fontsize=9)
    
#arrow_start = (21000,20000)
#arrow_end = (1000,1000)
    
#arrow = mplpatches.FancyArrowPatch(arrow_start, arrow_end,arrowstyle='->', mutation_scale=7, color='black', linewidth=1,)
#panel1.add_patch(arrow)


#plt.tight_layout()

rectangle1=mplpatches.Rectangle([100,100],4900,4900,
                                 linewidth=.7,
                                 edgecolor='black', facecolor='none', ls='--')
panel1.add_patch(rectangle1)

plt.savefig( f'{dir}{of}.png',dpi=600)
