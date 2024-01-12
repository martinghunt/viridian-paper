For xy scatterplot:

The directories are set up so that from `{path to viridian_paper repo}/code` running `python3 xy_scatterplot_manuscript.py -d . -vir figure_data/tree.intersection.viridian.optimized.mutations.tsv -gb figure_data/tree.intersection.gb.optimized.mutations.tsv -of reversion_comparison -r figure_data/NC_045512v2.fa` will produce `reversion_comparison.png` in `{path to viridian_paper repo}/code`.

This code assumes that mutation tables were already extracted from the Mutation Annotated Trees for each assembly. 
Mutation tables can be created with the following matUtils command (assuming usher is installed and setup as an environment path) `matUtils summary -i {path to .pb file} -m {path to output dir}.mutations.tsv'`

For more information on running `xy_scatterplot_manuscript.py` type `python3 xy_scatterplot_manuscript.py -h` from the `{path to viridian_paper repo}/code` directory.

For reversion threshold plot:

The directories are set up so that from `{path to viridian_paper repo}/code` running `python3 reversionthreshold.py -d . -vir figure_data/tree.intersection.viridian.optimized.mutations.tsv -gb figure_data/tree.intersection.gb.optimized.mutations.tsv -of reversion_comparison -r figure_data/NC_045512v2.fa` will produce `reversionthrehold.png` in `{path to viridian_paper repo}/code`.

This code assumes that mutation tables were already extracted from the Mutation Annotated Trees for each assembly. 
Mutation tables can be created with the following matUtils command (assuming usher is installed and setup as an environment path) `matUtils summary -i {path to .pb file} -m {path to output dir}.mutations.tsv'`

For more information on running `reversionthreshold.py` type `python3 reversionthreshold.py -h` from the `{path to viridian_paper repo}/code` directory.

`back-mutation.py`:
This code is called from inside the plotting scripts. It takes the mutation table and reference sequence and outputs a tsv of backmutations for the entire MAT.

`./figure_data`:
contains mutation tables from the September 2023 versions of the Mutation Annotated Trees
`tree.intersection.gb.optimized.mutations.tsv` was created from `Trees.20230905/tree.intersection.gb.optimized.pb`
`tree.intersection.viridian.optimized.mutations.tsv` was created from `Trees.20230905/tree.intersection.viridian.optimized.pb`
`NC_045512v2.fa` is the fasta file for the SARS-CoV-2 reference genome  





