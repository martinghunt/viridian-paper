#!/usr/bin/env python3

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("truth_set_scheme_scores.tsv", delimiter="\t")
df["Platform/scheme"] = df["platform"] + "/" + df["amplicon_scheme"]

plt.figure(figsize=(6, 3.5))
sns.scatterplot(data=df, x="best_score", y="second_best_score", hue="Platform/scheme")
min_x = min(df["best_score"])
max_xy = min(max(df["best_score"]), max(df["second_best_score"]))
plt.plot([0, max_xy], [0, max_xy], '--', linewidth=1, color="lightgray")
plt.plot([0, 2*max_xy], [0, max_xy], '-', linewidth=1, color="lightgray")
plt.xlabel("Best score")
plt.ylabel("Second best score")
plt.legend().remove()
plt.tight_layout()
plt.savefig("score_truth.scatter_scores.pdf")
plt.clf()

plt.figure(figsize=(6, 3.5))
sns.scatterplot(data=df, x="best_score", y="score_ratio", hue="Platform/scheme")
plt.axhline(y=0.5, color="gray", linestyle="--", linewidth=1)
plt.axvline(x=250, color="gray", linestyle="--", linewidth=1)
plt.legend(bbox_to_anchor=(1.05, 0.7), loc="upper left")
plt.xlabel("Best score")
plt.ylabel("Second best score / best score")
plt.tight_layout()
plt.savefig("score_truth.scatter_best_score_v_ratio.pdf")
plt.clf()
