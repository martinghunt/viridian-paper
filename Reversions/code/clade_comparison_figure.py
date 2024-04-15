import argparse
import os
import sys
import subprocess
import matplotlib.pyplot as plt

#create a dictionary for usa and uk for each file 
def read_parsed_intros(file_path):
    data_dict = {}
    with open(file_path, 'r') as file:
        # Skip header line
        header = file.readline().strip().split('\t')
        print(header)
        for line in file:
            columns = line.strip().split('\t')
            print(columns)
            key = columns[0]
            value = columns[1]

            # Check if key exists in the dictionary, if not, add it
            if key not in data_dict:
                data_dict[key] = {}

            # Check if value exists for the key, if not, add it
            if value not in data_dict[key]:
                data_dict[key][value] = 1
            else:
                # Increment the count if the value already exists
                data_dict[key][value] += 1

    return data_dict

def compute_percent_difference(data1, data2):
    percent_diff_dict = {}

    for key in data1:
        if key in data2:
            for value in data1[key]:
                count1 = data1[key].get(value, 0)
                count2 = data2[key].get(value, 0)

                # Compute percent difference for each value
                if count1 != 0:
                    diff = count1 - count2
                    percent_diff = (count1 - count2) / count1
                    print( key, value, count1, count2, diff, percent_diff, sep='\t' ) 

def compute_cdf(data_dict, output):
    cdf_dict = {}
    with open(output, 'w') as o:
        o.write('country\tcluster_size\tcumulative_samples\n')
        for key, inner_dict in data_dict.items():
            print(inner_dict)
            cumulative_counts = {}
            total_count = 0

            # Sort the inner dictionary keys in ascending order
            sorted_keys = sorted(inner_dict.keys(), key=lambda x: float(x))
            
            print(sorted_keys)
            for inner_key in sorted_keys:
                total_count += inner_dict[inner_key] * int( inner_key )
                cumulative_counts[inner_key] = total_count
                #print ( key, inner_key, total_count ) 
                o.write(f'{key}\t{inner_key}\t{total_count}\n')

            cdf_dict[key] = cumulative_counts

def read_tab_delimited_file(file_path):
    data_dict = {}
    with open(file_path, 'r') as file:
        # Skip header line
        header = file.readline().strip().split('\t')
        for line in file:
            columns = line.strip().split('\t')
            country = columns[0]
            clust_size = int(columns[1])
            cum_samps = int(columns[2])

            # Check if key exists in the dictionary, if not, add it
            
            if country == 'USA' or country == 'United Kingdom':
                if country not in data_dict:
                    data_dict[country] = [(clust_size, cum_samps)]
                else:
                    data_dict[country].append((clust_size, cum_samps))

    #print(data_dict)

    return data_dict



def make_figure(data_dict1, data_dict2, dir):
    print(data_dict1)
    usa_x1 = [i[0] for i in data_dict1['USA']]
    
    usa_y1 = [i[1] for i in data_dict1['USA']]
    uk_x1 = [i[0] for i in data_dict1['United Kingdom']]
    uk_y1 = [i[1] for i in data_dict1['United Kingdom']]
    usa_x2 = [i[0] for i in data_dict2['USA']]
    usa_y2 = [i[1] for i in data_dict2['USA']]
    uk_x2 = [i[0] for i in data_dict2['United Kingdom']]
    uk_y2 = [i[1] for i in data_dict2['United Kingdom']]
    print(usa_y1)
    #c1_list = []
    #c2_list = []
    #xs = []
    '''
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
                '''

    fig, axs = plt.subplots(nrows = 1, ncols= 2, figsize = (8,4),layout="constrained")
    panel1 = axs[0]
    panel2 = axs[1]
    #panel2.set_aspect('equal')
    #panel1.set_aspect('equal')
    panel1.set_xlabel('Cluster Size')
    panel1.set_ylabel('Cumulative Number of Samples')
    panel2.set_xlabel('Cluster Size')
    panel2.set_ylabel('Cumulative Number of Samples')
    panel1.set_title('USA')
    panel2.set_title('UK')
    #panel1.set_xlim(max(usa_x1[-1], usa_x2[-1]))
    #xlim=c(0.999999999999, )
    #panel1.set_xticks(['1])
    panel1.plot(usa_x1, usa_y1, c='b', label='Genbank', alpha=.5)
    panel1.plot(usa_x2, usa_y2, c='r', label='Viridian', alpha=.5)
    panel2.plot(uk_x1, uk_y1, c='b', label='Genbank', alpha=.5)
    panel2.plot(uk_x2, uk_y2, c='r', label='Viridian', alpha=.5)
    #panel1.set_ylim(max(usa_y1[-1], usa_y2[-1]))
    panel1.legend()
    panel1.set_xscale('log')
    panel1.set_yscale('log')
    panel2.set_xscale('log')
    panel2.set_yscale('log')
    #Viridian = panel1.plot(xs,c1_list, c='b', label='Viridian', alpha=.5)
    #Genbank = panel1.plot(xs, c2_list, c='r', label='Genbank', alpha=.5)
    panel2.legend()
    plt.savefig(f'{dir}clade_comparison.png',dpi=600)
    #if rm:
    #    os.system(f'rm {dir}/backmuts-*')



#process data and create figure
def main(vir, gb, dir):
    #subprocess.run("cat figure_data/tree.intersection.viridian.optimized.intros_clades.tsv | cut -f1,2 | perl -pe 's/_node_\d+//' | uniq -c | sed -E 's/^ *//; s/ /\t/' > figure_data/viridian.counts.tsv", shell=True)
    #subprocess.run("cat figure_data/tree.intersection.gb.optimized.intros_clades.tsv | cut -f1,2 | perl -pe 's/_node_\d+//' | uniq -c | sed -E 's/^ *//; s/ /\t/' > figure_data/gb.counts.tsv", shell=True)
    #cmd = f"""cat {gb} | cut -f10,2 | awk -F'\t' '{{print $2 "\t" $1}}' > {datadir}gb.counts.tsv"""
    #subprocess.run(cmd, shell=True)
    #cmd = f"""cat {vir} | cut -f10,2 | awk -F'\t' '{{print $2 "\t" $1}}' > {datadir}viridian.counts.tsv"""
    #subprocess.run( cmd, shell=True)
    #file1_path = f'{datadir}gb.counts.tsv'
    #file2_path = f'{datadir}viridian.counts.tsv'

    # Read data from the first file
    data1 = read_parsed_intros(gb)
    
    # Read data from the second file
    data2 = read_parsed_intros(vir)
    #compute_percent_difference(data1, data2)
    #print(data1)
    cdf1 = compute_cdf(data1, f'{dir}gb.cumulative.tsv') 
    cdf2 = compute_cdf(data2, f'{dir}vir.cumulative.tsv') 

    
    #contains all positions and their counts including counts of 0
    gb_data = read_tab_delimited_file(f'{dir}gb.cumulative.tsv')
    vir_data = read_tab_delimited_file(f'{dir}vir.cumulative.tsv')
    make_figure(gb_data, vir_data, dir)
    

    

#create args
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('-dd', '--data_directory', required=True, type=str, help='directory for all data (make sure this directory will have enough space!!!!)')

    parser.add_argument('-d', '--working_directory', required=True, type=str, help='directory for all outputs (make sure this directory will have enough space!!!!)')
    #parser.add_argument('-of', '--outfile', required=True, type=str, help='name for output file-omit suffix (make sure this directory will have enough space!!!!)')
    #parser.add_argument('-r', '--ref_file', required=True, type=str, help="path to reference fasta file")
    parser.add_argument('-vir', '--viridian_intros', required=True, type=str, help="path to mutation file for mat1")
    parser.add_argument('-gb', '--genbank_intros', required=True, type=str, help="path to mutation file for mat2")
    #parser.add_argument('-rm', '--remove_files', required=False, default=False, type=bool, help="if True, remove backmutation files created for analysis")

    args = parser.parse_args()
    dir = args.working_directory
    if not dir.endswith('/'):
        dir = dir+'/'
    #ref = args.ref_file
    vir = args.viridian_intros
    gb = args.genbank_intros
    #of = args.outfile
    #rm = args.remove_files
    #datadir = args.data_directory
    #software_dir = '/'.join(sys.argv[0].split('/')[:-1])+'/'
    #if datadir[-1] != '/':
    #    datadir = datadir +'/'
    #print(datadir)
    #m2name = m2.split('/')[-1][:-4]

    #keep software as unit
    #software_dir = '/'.join(sys.argv[0].split('/')[:-1])+'/'
    #if software_dir == '/':
    #    software_dir = './'

    main(vir, gb, dir)




