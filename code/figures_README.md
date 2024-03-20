# Figures for Viridian Manuscript 

## For Reversion Analysis

### Reversion Analysis Figure Data:

This repo contains several Datasets from different iterations of the data. The most current is `Dataset.v04`.
`Dataset.v04` contains mutation tables from Mutation Annotated Trees created from the most recent pipeline.
`tree.intersection.gb.optimized.mutations.tsv` was created from the most recent version of `tree.intersection.gb.optimized.pb` (not included in repo due to size restriction)
`tree.intersection.viridian.optimized.mutations.tsv` was created from `tree.intersection.viridian.optimized.pb` (also not included)
`NC_045512v2.fa` is the fasta file for the SARS-CoV-2 reference genome 

### For xy scatterplot:

The directories are set up so that from `{path to viridian-paper repo}/code` running `python3 xy_scatterplot_manuscript.py -d . -vir {path to figure data}/tree.intersection.viridian.optimized.mutations.tsv -gb {path to figure data}/tree.intersection.gb.optimized.mutations.tsv -of xy_plot -r {path to figure data}/NC_045512v2.fa` will produce `xy_plot.png` in `{path to viridian_paper repo}/code`.

This code assumes that mutation tables were already extracted from the Mutation Annotated Trees for each assembly. 
Mutation tables can be created with the following matUtils command (assuming UShER is installed and setup as an environment path) `matUtils summary -i {path to .pb file} -m {path to output dir}.mutations.tsv'`

For more information on running `xy_scatterplot_manuscript.py` type `python3 xy_scatterplot_manuscript.py -h` from the `{path to viridian_paper repo}/code` directory.

### For reversion threshold plot:

The directories are set up so that from `{path to viridian_paper repo}/code` running `python3 reversionthreshold.py -d . -vir {path to figure data}/tree.intersection.viridian.optimized.mutations.tsv -gb {path to figure data}/tree.intersection.gb.optimized.mutations.tsv -of reversion_comparison -r {path to figure data}/NC_045512v2.fa` will produce `reversionthrehold.png` in `{path to viridian_paper repo}/code`.

This code assumes that mutation tables were already extracted from the Mutation Annotated Trees for each assembly. 
Mutation tables can be created with the following matUtils command (assuming usher is installed and setup as an environment path) `matUtils summary -i {path to .pb file} -m {path to output dir}.mutations.tsv'`

For more information on running `reversionthreshold.py` type `python3 reversionthreshold.py -h` from the `{path to viridian_paper repo}/code` directory.

### `back-mutation.py`:

This code is called from inside the plotting scripts. It takes the mutation table and reference sequence and outputs a tsv of backmutations for the entire MAT.

## For the Viral Introduction Analysis:

### Viral Introduction Analysis Figure Data

This repo contains several Datasets from different iterations of the data. The most current is `Dataset.v04`.
Introduction information is extracted from the Mutation Annnotated Tree using `matUtils introduce -i {mutation annotated tree} -s {sample regional metadata} -o {output file for introduction info}`

For `tree.intersection.viridian.optimized.pb` sample regional metadata is `introducemetadata.tsv`
For `tree.intersection.gb.optimized.pb` sample regional metadata is `introducemetadata.gb.tsv`

introduction clade data for gb was made with `matUtils introduce -i tree.intersection.gb.optimized.pb -s introducemetadata.gb.tsv -u gb.intros.tsv`

introduction clade data for viridian was made with `matUtils introduce -i tree.intersection.viridian.optimized.pb -s introducemetadata.tsv -u vir.intros.tsv`

To identify numbers and sizes of clades:
`cat vir.intros.tsv | cut -f1,2 | perl -pe 's/_node_\d+//' > vir.counts.tsv`
`cat gb.intros.tsv | cut -f1,2 | perl -pe 's/_node_\d+//' > gb.counts.tsv`

### code/clade_comparison_figure.py:

From `{path to viridian-paper repo}/code` running `py clade_comparison_figure.py -d {path to output directory}  -vir {path to directory for data}/vir.counts.tsv -gb {path to dir for data}/gb.counts.tsv -dd {path to directory for data}` will produce `clade_comparison.png` in `{path to viridian-paper repo}/code`

### code/intro_table.py
Creates the table of introduction counts for the US and UK for each database. 

Format data for code: 
`awk -F '\t' '{print $10}' ../Dataset.v04/figure_data/gb.intros.tsv | sort | uniq -c > ../Dataset.v04/figure_data/gb_introtable.tsv`
`awk -F '\t' '{print $10}' ../Dataset.v04/figure_data/vir.intros.tsv | sort | uniq -c > ../Dataset.v04/figure_data/vir_introtable.tsv`

`cat ../Dataset.v04/figure_data/gb_introtable.tsv | perl -pe 's/^\s+//' | perl -pe 's/ /\t/g' | awk '{$1=$1; sub(/ /, "\t")}1' > ../Dataset.v04/figure_data/gb_introtable_format.tsv`
`cat ../Dataset.v04/figure_data/vir_introtable.tsv | perl -pe 's/^\s+//' | perl -pe 's/ /\t/g' | awk '{$1=$1; sub(/ /, "\t")}1' > ../Dataset.v04/figure_data/vir_introtable_format.tsv`
`join -t $'\t' -1 2 -2 2 ../Dataset.v04/figure_data/vir_introtable_format.tsv ../Dataset.v04/figure_data/gb_introtable_format.tsv | sort -n -r -k 3,3 > fullintros.tsv`
`sort -t$'\t' -k3,3nr fullintros.tsv > fullintros_sorted.tsv` 

Delete 'region' row of `fullintros_sorted.tsv`: 
`nano fullintros_sorted.tsv`

run this command to create `intro_comparison_table.png` in your current directory
`py ~/scripts/viridian-paper/code/intro_table.py introtable_joined_sorted.tsv` 










