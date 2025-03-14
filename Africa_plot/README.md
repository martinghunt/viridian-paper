# Africa dataset main figures showing errors

The figure was made using this fork/branch `qc_plots` of the `viridian`
github repository:
https://github.com/martinghunt/viridian/tree/qc_plots
Git commit b7399f932d91be21f7a13f924b3d7eaaee347de3 was used.

The data was gathered into a pickle file per data set using the command
`viridian combine_data`. These four pickle files are in this directory.

The main figure was then made with the command:

```
PYTHONPATH=~/Home/git/viridian python3 -m viridian qc_plot one_stat_plot \
   --gene_track --outdir Out \
   'viridian:#40826D:Viridian/gisaid:#d95f02:Original/connor:#7570b3:ARTIC-ILM/epi2me:#e7298a:ARTIC-ONT' \
   "Illumina, ARTIC-V3/Illumina, ARTC-V4.1/Nanopore, ARTIC-V3/Nanopore, Midnight" \
   ilm_artic3.pickle ilm_artic4.1.pickle \
   ont_artic3.pickle ont_midnight.pickle
```


Files are written to the (created by the script) output directory `Out/`, which
is included in this repo.

The bar charts `africa.bar_Total_errors.pdf`, `africa.bar_Sites_with_error.pdf`
and supplementary table `suppl_table.tsv`  were made with:
```
PYTHONPATH=~/Home/git/viridian ./make_suppl_table_and_plots.py
```
