import matplotlib.pyplot as plt
from matplotlib.table import table
import pandas as pd
import sys

file_path = sys.argv[1]

colnames = ['Country', 'Number of Introductions (Vir)', 'Number of Introductions (GB)']
# Read data from a TSV file
#file_path = 'your_data.tsv'  # Replace with your TSV file path
data = pd.read_csv(file_path, sep='\t', header=None)

# Create a Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=False)
  # Adjust the scaling factor

# Plotting the table
table_data = []
print(list(data.columns))
#pd.set_option('display.max_colwidth', None)
for row in data.values:
    d = list(row)
    '''
    print(d)
    if not d[0] == '...':
        #table_data.append(list(row))
        d[1] = int(d[1])
        d[2] = int(d[2])
        d[3] = int(d[3])
        d[4] = int(d[4])
        d[5] = round(d[5], 4)
    else:
        #table_data.append(list(row))
        d[1] = '...'
        d[2] = '...'
        d[3] = '...'
        d[4] = '...'
        d[5] = '...'
    print(d)
    '''
    table_data.append(d)



table = table(ax, cellText=table_data, colLabels=colnames, loc='center')
table.auto_set_font_size(False)
#table.scale(1.0, 1.0)
table.set_fontsize(10)
table.scale(1.25, 1.4)  # Adjust the scale for better readability

# Removing axis labels
ax.axis('off')

# Adding a title to the table

fig.suptitle(f'Number of Inferred Viral Introductions for Viridian and Genbank Datasets', y=.92 )

# Display the table
plt.savefig( f'intro_comparison_table.png',dpi=600)