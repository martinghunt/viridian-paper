import argparse
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse

#import math

#count reversions at each position of genome across the whole tree
def make_histo(mutname, ref_seq):
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
    #convert histogram to a list the length of the SARS-CoV-2 genome. Each index of the list corresponds to the 0-index position of SARS
    counts = []
    for i in range(1, len(ref_seq)+1):
        if i not in histo:
            counts.append(0)
        else:
            counts.append(histo[i])

    return counts

#process data and make plot
def main(dir, ref, m1, m2, of, m1name, m2name, software_dir, rm):
    #make backmut1
    os.system(f'python3 {software_dir}back-mutation.py -f {ref} -m {m1} -o {dir} -n {m1name}')
    #make backmut2
    os.system(f'python3 {software_dir}back-mutation.py -f {ref} -m {m2} -o {dir} -n {m2name}')
    ref_seq = ''
    with open(ref) as r:
        for line in r:
            if not line.startswith('>'):
                line = line.strip()
                ref_seq += line

    counts1 = make_histo(m1name, ref_seq)
    counts2 = make_histo(m2name, ref_seq)

    assert len(counts1) == len(counts2)
    sortedc1 = sorted(counts1)
    sortedc2 = sorted(counts2)

    #identify outliers for left plot
    outsc1 = sortedc1[-3:]
    outsc2 = sortedc2[-3:]

    outs = []
    for c in outsc1:
        ind = counts1.index(c)
        outs.append((c,counts2[ind],ind))

    for c in outsc2:
        ind = counts2.index(c)
        outs.append((counts1[ind],c,ind))

    #identify outliers for right plot
    outs_zoom = []
    sc1_zoom = [i for i in counts1 if i>100 and i < 5000 and counts2[counts1.index(i)] < 5000 and counts2[counts1.index(i)] > 100]
    sc2_zoom = [i for i in counts2 if i>100 and i < 5000 and counts1[counts2.index(i)] < 5000 and counts1[counts2.index(i)] > 100]
    outsc1_zoom = sorted(sc1_zoom)[-3:]
    outsc2_zoom = sorted(sc2_zoom)[-3:]

    for c in outsc1_zoom:
        ind = counts1.index(c)
        outs_zoom.append((c,counts2[ind],ind))

    for c in outsc2_zoom:
        ind = counts2.index(c)
        outs_zoom.append((counts1[ind],c,ind))

    #make plots
    fig, axs = plt.subplots(nrows = 1, ncols= 2, figsize = (8,4),layout="constrained")
    panel1 = axs[0]
    panel2 = axs[1]
    panel2.set_aspect('equal')
    panel1.set_aspect('equal')
    panel1.set_xlabel('Reversion Counts in Viridian')
    panel1.set_ylabel('Reversion Counts in Genbank')
    panel2.set_xlabel('Reversion Counts in Viridian')
    panel2.set_ylabel('Reversion Counts in Genbank')

    panel1.scatter(counts1, counts2, s=5, c='b', marker="o", label='second', alpha=.2)

    #plot y=x line
    panel1.axline((0, 0), slope=1, alpha=.7)

    #optional log scale
    #panel1.set_yscale("log")
    #panel1.set_xscale("log")
    panel1.set_ylim(panel1.get_xlim())
    panel2.scatter(counts1, counts2, s=5, c='b', marker="o", label='second', alpha=.2)
    panel2.set_xlim(100,5000)
    panel2.set_ylim(100,5000)
    panel2.axline((0, 0), slope=1, alpha=.7)

    rectangle1=mplpatches.Rectangle([100,100],790,990,
                                    linewidth=.7,
                                    edgecolor='black', facecolor='none', ls='--')

    panel2.spines['top'].set_linestyle(':')
    panel2.spines['right'].set_linestyle(':')
    panel2.spines['bottom'].set_linestyle(':')
    panel2.spines['left'].set_linestyle(':')


    # Set arrow properties
    arrow_length = 3000
    label_offset = 500

    # Create arrows pointing to each coordinate in outs (for left plot)
    #conditionals adjust arrow placement for certain positions
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
        panel1.text(arrow_start[0], arrow_start[1] , f'{o[2]+1}', ha='center', va='bottom', fontsize=9)

    # Create arrows pointing to each coordinate in outs_zoom (for right plot)
    #conditionals adjust arrow placement for certain positions
    arrow_length = 500
    label_offset = 50
    for o in outs_zoom:
        arrow_end = (o[0], o[1] + label_offset)
        arrow_start = (o[0], o[1]+ arrow_length + label_offset)
        if o[2] == 240:
            arrow_end = (o[0], o[1] + label_offset)
            arrow_start = (o[0] + 150, o[1]+ arrow_length + label_offset - 75)
        if o[2] == 22812:
            arrow_end = (o[0], o[1] + label_offset)
            arrow_start = (o[0] + 550, o[1]+ arrow_length + 200 + label_offset)
        if o[2] == 24409:
            arrow_end = (o[0], o[1] + label_offset)
            arrow_start = (o[0] + 400, o[1]+ arrow_length + 600 + label_offset)
        if o[2] == 27637:
            arrow_end = (o[0], o[1] + label_offset)
            arrow_start = (o[0] + 500, o[1]+ arrow_length + 0 + label_offset)


        arrow = mplpatches.FancyArrowPatch(arrow_start, arrow_end,
                                arrowstyle='->', mutation_scale=7, color='black', linewidth=1)
        panel2.add_patch(arrow)
        panel2.text(arrow_start[0], arrow_start[1], f'{o[2]+1}', ha='center', va='bottom', fontsize=9)

    #add rectangle to left plot to indicate zoomed in spot
    rectangle1=mplpatches.Rectangle([100,100],4900,4900,
                                    linewidth=.7,
                                    edgecolor='black', facecolor='none', ls='--')
    panel1.add_patch(rectangle1)

    plt.savefig( f'{dir}{of}.png',dpi=600)
    plt.savefig( f'{dir}{of}.pdf')
    if rm:
        os.system(f'rm {dir}/backmuts-*')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--working_directory', required=True, type=str, help='directory for all outputs (make sure this directory will have enough space!!!!)')
    parser.add_argument('-of', '--outfile', required=True, type=str, help='name for output file-omit suffix (make sure this directory will have enough space!!!!)')
    parser.add_argument('-r', '--ref_file', required=True, type=str, help="path to reference fasta file")
    parser.add_argument('-vir', '--viridian_mutations', required=True, type=str, help="path to mutation file for viridian MAT")
    parser.add_argument('-gb', '--genbank_mutations', required=True, type=str, help="path to mutation file for genbank MAT")
    parser.add_argument('-rm', '--remove_files', required=False, default=False, type=bool, help="if True, remove all mutation files created for analysis, (mutation files created in mat directory)")


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
    #print(m1name)
    #print(m2name)

    #keep software as unit
    software_dir = '/'.join(sys.argv[0].split('/')[:-1])+'/'
    if software_dir == '/':
        software_dir = './'

    rm = args.remove_files
    main(dir, ref, m1, m2, of, m1name, m2name, software_dir, rm)




