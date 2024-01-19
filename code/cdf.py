def read_tab_delimited_file(file_path):
    data_dict = {}
    with open(file_path, 'r') as file:
        # Skip header line
        header = file.readline().strip().split('\t')
        for line in file:
            columns = line.strip().split('\t')
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
	

def compute_percent_difference(data1, data2):
    percent_diff_dict = {}

    for key in data1:
        if key in data2:
            for value in data1[key]:
                count1 = data1[key].get(value, 0)
                count2 = data2[key].get(value, 0)

                # Compute percent difference for each value
                if count1 != 0 :
                    diff = count1 - count2
                    percent_diff = (count1 - count2) / count1
                    print( key, value, diff, percent_diff ) 

def main():
    # File paths
    file1_path = 'gb.counts.txt'
    file2_path = 'vir.counts.txt'

    # Read data from the first file
    data1 = read_tab_delimited_file(file1_path)

    # Read data from the second file
    data2 = read_tab_delimited_file(file2_path)

    # Compute percent difference
    #compute_percent_difference(data1, data2)

    ## compute and print the CDF 
    cdf1 = compute_cdf(data1, 'figure_data/gb.cumulative.tsv') 
    cdf2 = compute_cdf(data2, 'figure_data/vir.cumulative.tsv') 

if __name__ == "__main__":
    main()