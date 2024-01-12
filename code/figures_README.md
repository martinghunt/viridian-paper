For xy scatterplot:

The directories are set up so that from `{path to viridian_paper repo}/code` running py `xy_scatterplot_manuscript.py -d . -vir figure_data/tree.intersection.viridian.optimized.mutations.tsv -gb figure_data/tree.intersection.gb.optimized.mutations.tsv -of reversion_comparison -r figure_data/NC_045512v2.fa` will produce `reversion_comparison.png` in `{path to viridian_paper repo}/code`.

This code assumes that mutation tables were already extracted from the Mutation Annotated Trees for each assembly. 
Mutation tables can be created with the following matUtils command (assuming usher is installed and setup as an environment path) `matUtils summary -i {path to .pb file} -m {path to output dir}.mutations.tsv'`

For more information on running `xy_scatterplot_manuscript.py` type `xy_scatterplot_manuscript.py -h` from the `{path to viridian_paper repo}/code` directory.

For reversion threshold plot:

The directories are set up so that from `{path to viridian_paper repo}/code` running py `reversionthreshold.py -d . -vir figure_data/tree.intersection.viridian.optimized.mutations.tsv -gb figure_data/tree.intersection.gb.optimized.mutations.tsv -of reversion_comparison -r figure_data/NC_045512v2.fa` will produce `reversionthrehold.png` in `{path to viridian_paper repo}/code`.

This code assumes that mutation tables were already extracted from the Mutation Annotated Trees for each assembly. 
Mutation tables can be created with the following matUtils command (assuming usher is installed and setup as an environment path) `matUtils summary -i {path to .pb file} -m {path to output dir}.mutations.tsv'`

For more information on running `reversionthreshold.py` type `reversionthreshold.py -h` from the `{path to viridian_paper repo}/code` directory.



