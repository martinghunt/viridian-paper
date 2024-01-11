import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fasta_file', required=True, type=str, help='path to reference fasta')
parser.add_argument('-m', '--mutation_file', required=True, type=str, help='path to mutation list')
parser.add_argument('-o', '--out_dir', required=True, help='path to output directory')
parser.add_argument('-n', '--out_file', required=True, help='name for output file')
args = parser.parse_args()

fasta = args.fasta_file
muts = args.mutation_file
o = args.out_dir
name = args.out_file

if o[-1] != '/':
    o = o + '/'

#genome positions are 1-indexed
def parse_ref(fasta_file):
    with open(fasta_file) as F:
        ref = {}
        pos = 1
        for line in F:
            if not line.startswith('>'):
                line = line.strip()
                #print(len(line))
                for c in line:
                    ref[pos] = c
                    pos += 1
    return ref

#currently making the assumption that all muts are snps (can change later if needed)
def getback_muts(muts_file, ref_dict):
    #backs stores actual mutations
    backs = {}
    mutations = 0
    backmuts = 0 
    #print(muts_file)
    with open(muts_file, 'r') as m:
        for line in m:
            if not line.startswith('ID'):
                line = line.strip().split()
                #print(line)
                count = line[1]
                mutations += int(count)
                next = line[0][-1]
                position = int(line[0][1:-1])
                #print(line)
                if next == ref_dict[position]:
                    prev = line[0][0]
                    if (position, next) not in backs:
                        backs[(position, next)] = {prev:count}
                    else:
                        backs[(position, next)][prev] = count
                    backmuts += int(count)

    return mutations, backmuts, backs

ref = parse_ref(fasta)
#print(ref)
mutations, backmuts, backs = getback_muts(muts, ref)
print('mutations', mutations)
print('backmuts', backmuts)
print('backmut rate', backmuts/mutations)
#print(backs)


output = []
for b in backs:
    for n in backs[b]:
        output.append([b[0], n, b[1], str(backs[b][n])])

sorted_outputs = sorted(output, key=lambda x: x[0])

#for o in sorted_outputs:
#    print(o)



with open(f'{o}backmuts-{name}', 'w') as out:
    out.write('position\tprev_allele\tnew_allele(reference_nuc)\tcounts\n')
    for o in sorted_outputs:
        o[0] = str(o[0])
        o = '\t'.join(o)
        out.write(f"{o}\n")
        
        


