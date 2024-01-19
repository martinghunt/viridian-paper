import argparse
import os
import sys
import matplotlib.pyplot as plt

#create a reversion count for every position in SARS-CoV-2 genome
def make_histo(mutname, ref_seq):
    histo = {}
    with open(f'{dir}/backmuts-{mutname}') as f:
        line=f.readline()
        for line in f:
            line = line.strip().split()
            if int(line[0]) not in histo:
                histo[int(line[0])] = int(line[3])
            else:
                histo[int(line[0])] += int(line[3])
    counts = []          
    for i in range(1, len(ref_seq)+1):
        if i not in histo:
            counts.append(0)
        else:
            counts.append(histo[i])
            if histo[i] > 6000:
                print(histo[i])
    return sorted(counts, reverse = True)


#process data and create figure
def main(dir, ref, m1, m2, of, rm):
    m1name = m1.split('/')[-1][:-4]
    m2name = m2.split('/')[-1][:-4]
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

    #contains all positions and their counts including counts of 0
    counts1 = make_histo(m1name, ref_seq)
    counts2 = make_histo(m2name, ref_seq) 

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

    figureHeight=6
    figureWidth=6

    panel1Width=5
    panel1Height=5

    relativePanel1Width=panel1Width/figureWidth
    relativePanel1Height=panel1Height/figureHeight

    panel1=plt.axes([0.1,0.1,relativePanel1Width,relativePanel1Height])
    panel1.set_ylabel('Number of Genomic Positions Above Reversion Threshold')
    panel1.set_xlabel('Reversion Threshold')
    panel1.set_title('Genomic Positions Above a Certain Threshold of Reversions')

    #panel1.plot(x1, tots1, c='b', label='second', alpha=.5)
    #panel1.plot(x2, tots2, c='r', label='second', alpha=.5)
    panel1.set_ylim(0,250)
    #plt.legend()
    #panel2.set_xlim(0,10)
    Viridian = panel1.plot(xs,c1_list, c='b', label='Viridian', alpha=.5)
    Genbank = panel1.plot(xs, c2_list, c='r', label='Genbank', alpha=.5)
    plt.legend()
    plt.savefig( f'{dir}{of}.png',dpi=600)
    if rm:
        os.system(f'rm {dir}/backmuts-*')

#create args
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--working_directory', required=True, type=str, help='directory for all outputs (make sure this directory will have enough space!!!!)')
    parser.add_argument('-of', '--outfile', required=True, type=str, help='name for output file-omit suffix (make sure this directory will have enough space!!!!)')
    parser.add_argument('-r', '--ref_file', required=True, type=str, help="path to reference fasta file")
    parser.add_argument('-vir', '--viridian_mutations', required=True, type=str, help="path to mutation file for mat1")
    parser.add_argument('-gb', '--genbank_mutations', required=True, type=str, help="path to mutation file for mat2")
    parser.add_argument('-rm', '--remove_files', required=False, default=False, type=bool, help="if True, remove backmutation files created for analysis")

    args = parser.parse_args()
    dir = args.working_directory
    if not dir.endswith('/'):
        dir = dir+'/'
    ref = args.ref_file
    m1 = args.viridian_mutations
    m2 = args.genbank_mutations
    of = args.outfile
    rm = args.remove_files
    m1name = m1.split('/')[-1][:-4]
    m2name = m2.split('/')[-1][:-4]

    #keep software as unit
    software_dir = '/'.join(sys.argv[0].split('/')[:-1])+'/'
    if software_dir == '/':
        software_dir = './'

    main(dir, ref, m1, m2, of, rm)




