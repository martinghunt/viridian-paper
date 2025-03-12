# Maps and country counts

## Preprint version 1 April 2024

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

## Preprint version 2 September 2024

The maps were made with:

```
./make_maps.2.py run_metadata.v05.tsv.gz map.20240918
```

`run_metadata.v05.tsv.gz` available from Figshare.

The output files of the script are also included here:
* `maps.20240918.world.pdf` - world map
* `maps.20240918.europe.pdf` - Europe map
* `maps.20240918.legend.pdf` - legend for the maps
* `maps.20240918.suppl_counts.tsv` - supplementary table of country counts
