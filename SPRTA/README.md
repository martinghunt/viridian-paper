# Global tree Maple/SPRTA analysis

This folder has the script used to parse the Maple/SPRTA output file
`global_viridian_tree_maple_SPRTA_metadata.tsv.xz`, which is available
from Figshare: https://doi.org/10.6084/m9.figshare.28985573.v1

The script assumes that the file
`global_viridian_tree_maple_SPRTA_metadata.tsv.xz`
is in the current working directory. Then run the script with no options:

```
./make_histogram.py
```

It outputs to the terminal:
```
number of internal nodes: 750709
internal at least 99: 530514
internal percent at least 99: 70.66839481077221

number of leaf nodes: 1383934
leaves at least 99: 1013272
leaves percent at least 99: 73.21678634963806

number of nodes: 2134643
nodes at least 99: 1543786
nodes percent at least 99: 72.32057069964392
```

The script makes the files:
* `suppl_table.tsv`, which is in the supplementary spreadsheet
* `histogram.pdf`, which is in the supplementary pdf file

These output files are included here in this github repository.
