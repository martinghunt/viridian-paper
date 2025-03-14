#!/usr/bin/env python3

import pickle
import viridian
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


BC = viridian.qc_plots.Basecall

def stats_from_one_pickle(pickle_file):
    with open(pickle_file, "rb") as f:
        data = pickle.load(f)
    results = {}
    for dataset in data:
        errors = [x[BC.ACGT_BAD.value] for x in data[dataset].calls]
        results[dataset] = {
            "Total_errors": sum(errors),
            "Sites_with_error": len([x for x in errors if x>0]),
        }
    return results


pickle_files = {
    "ilm_artic3.pickle": "Illumina, ARTIC-V3",
    "ilm_artic4.1.pickle": "Illumina, ARTIC-V4",
    "ont_artic3.pickle": "Nanopore, ARTIC-V3",
    "ont_midnight.pickle": "Nanopore, Midnight",
}

tools = {
    "viridian": "Viridian",
    "gisaid": "Original",
    "connor": "ARTIC-ILM",
    "epi2me": "ARTIC-ONT",
}


stat_keys = ["Total_errors", "Sites_with_error"]
suppl_table_tsv = "suppl_table.tsv"
results = {}

with open(suppl_table_tsv, "w") as f:
    print("Dataset", "Tool", *stat_keys, sep="\t", file=f)
    for pickle_file, dataset in pickle_files.items():
        new_results = stats_from_one_pickle(pickle_file)
        results[dataset] = {}
        for tool in tools:
            if tool in new_results:
                print(dataset.replace("V4", "V4.1"), tools[tool], *[new_results[tool][x] for x in stat_keys], sep="\t", file=f)
                results[dataset][tools[tool]] = new_results[tool]


colours = {
    "Viridian": "#40826D",
    "Original": "#d95f02",
    "ARTIC-ILM": "#7570b3",
    "ARTIC-ONT": "#e7298a",
}

datasets = [
    "Illumina, ARTIC-V3",
    "Illumina, ARTIC-V4",
    "Nanopore, ARTIC-V3",
    "Nanopore, Midnight",
]

x_labels = [
    "Illumina, ARTIC-V3",
    "Illumina, ARTIC-V4.1",
    "Nanopore, ARTIC-V3",
    "Nanopore, Midnight",
]

tools = [
    "Viridian",
    "Original",
    "ARTIC-ILM",
    "ARTIC-ONT",
]

bar_colours = {
    "Illumina": [colours[x] for x in tools if "ONT" not in x],
    "Nanopore": [colours[x] for x in tools if "ILM" not in x],
}

x_label_pos = np.arange(4)
bar_width = 0.3
plt.style.use("seaborn-v0_8-whitegrid")
legend_patches = [mpatches.Patch(color=color, label=name) for name, color in colours.items()]

for stat in ["Total_errors", "Sites_with_error"]:
    fix, ax = plt.subplots(figsize=(4,3))
    ax.grid(False, axis="x")
    x_ticks = []

    for group_no, dataset in enumerate(datasets):
        res = results[dataset]
        bar_heights = [res[tool][stat] for tool in tools if tool in res]
        cols = bar_colours[dataset.split(",")[0]]
        bar_x  = [group_no + i * bar_width for i in range(3)]
        x_ticks.append(group_no + 0.3)
        ax.bar(bar_x, bar_heights, bar_width, color=cols)

    ax.legend(handles=legend_patches, facecolor="white", edgecolor="gray", frameon=True, framealpha=1)

    ax.set_ylabel(stat.replace("_", " "))
    ax.set_xticks(x_ticks,  x_labels)
    plt.setp(ax.get_xticklabels(), rotation=45, size=7)

    plt.tight_layout()
    plt.savefig(f"africa.bar_{stat}.pdf")

