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

def main():
    # File paths
    file1_path = 'gb.counts.txt'
    file2_path = 'vir.counts.txt'

    # Read data from the first file
    data1 = read_tab_delimited_file(file1_path)

    # Read data from the second file
    data2 = read_tab_delimited_file(file2_path)

    # Compute percent difference
    compute_percent_difference(data1, data2)

if __name__ == "__main__":
    main()