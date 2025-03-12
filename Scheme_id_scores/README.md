# Viridian scheme ID scores analysis

This code reproduces the supplementary data and plots showing scheme ID scores
on simulated reads and the empirical truth data set.

The simulated reads results and plots were made with:
```
./sims_run_analysis.py viridian_v1.3.1.img score_sims
```
where `viridian_v1.3.1.img` is the Viridian singularity container.
The script writes files to `score_sims.*`.


The empirical truth data set data is in the file `truth_set_scheme_scores.tsv`,
which is also in the supplementary spreadsheet.
The plots were made from this file (the input file is hard-coded) with:
```
./truth_set_scheme_scores.plots.py
```
