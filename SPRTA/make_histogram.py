#!/usr/bin/env python3

import matplotlib
import csv
import sys
from xopen import xopen
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

csv.field_size_limit(sys.maxsize)


def millions(x, pos):
    return f"{round(x * 1e-6, 2)}"


hist_internal = [0] * 101
hist_leaves = [0] * 101

run_prefixes = {"ERR", "SRR", "DRR"}

with xopen("global_viridian_tree_maple_SPRTA_metadata.tsv.xz", "rt") as f:
    for d in csv.DictReader(f, delimiter="\t"):
        if d["support"] == "":
            continue

        support = int(100 * float(d["support"]))

        if d["strain"][:3] in run_prefixes:
            hist_leaves[support] += 1
        else:
            assert d["strain"].startswith("in") or d["strain"].startswith("node_")
            hist_internal[support] += 1


with open("suppl_table.tsv", "w") as f:
    print("Support", "Internal_node", "Leaf_node", sep="\t", file=f)
    for i in range(0, 101):
        print(i, hist_internal[i], hist_leaves[i], sep="\t", file=f)


x = list(range(101))
plt.figure(figsize=(6, 3))
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(millions))

common_opts = {"width": 0.79, "linewidth": 0.5, "edgecolor": "black"}
plt.bar(x, hist_internal, label="Internal nodes", color="black", **common_opts)
plt.bar(
    x,
    hist_leaves,
    bottom=hist_internal,
    label="Leaves",
    color="lightgray",
    **common_opts,
)
plt.yticks(list(range(0, 1_501_000, 250_000)))
plt.legend()
plt.xlabel("Percent Support")
plt.ylabel("Number of nodes (millions)")
plt.tight_layout()
plt.savefig("histogram.pdf", format="pdf")

total_internal = sum(hist_internal)
total_leaves = sum(hist_leaves)
at_least_99_internal = sum(hist_internal[-2:])
at_least_99_leaves = sum(hist_leaves[-2:])

print("number of internal nodes:", total_internal)
print("internal at least 99:", at_least_99_internal)
print("internal percent at least 99:", 100 * at_least_99_internal / total_internal)
print()
print("number of leaf nodes:", total_leaves)
print("leaves at least 99:", at_least_99_leaves)
print("leaves percent at least 99:", 100 * at_least_99_leaves / total_leaves)
print()
total = total_internal + total_leaves
total_99 = at_least_99_internal + at_least_99_leaves
print("number of nodes:", total)
print("nodes at least 99:", total_99)
print("nodes percent at least 99:", 100 * total_99 / total)
