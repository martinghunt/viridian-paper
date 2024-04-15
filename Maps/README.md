# Maps and country counts

To reproduce the world map (main figure), map of Europe (supplementary
figure), and the supplementary table of country counts, run:

```
./make_maps.py run_metadata.v04.tsv.gz maps.20240319
```

Note that `run_metadata.v04.tsv.gz` is available separately on Figshare, as
it is too big to include here.

The output files of the script are also included here:
* `maps.20240319.world.pdf` - world map
* `maps.20240319.europe.pdf` - Europe map
* `maps.20240319.legend.pdf` - legend for the maps
* `maps.20240319.suppl_counts.tsv` - supplementary table of country counts
