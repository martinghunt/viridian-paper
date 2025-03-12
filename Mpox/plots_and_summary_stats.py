#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr


df = pd.read_csv("results.tsv", delimiter="\t")


plt.figure(figsize=(6, 3))
ax = sns.histplot(data=df, x="CT_value", hue="viridian_result", binwidth=1) #, multiple="stack")
ax.legend_.set_title("Viridian result")
plt.xlabel("CT Value")
plt.ylabel("Number of samples")
plt.tight_layout()
plt.savefig("mpox.ct_hist.pdf")


plt.figure(figsize=(6, 3))
sns.histplot(data=df, x="consensus_length")
plt.xlabel("Viridian consensus length")
plt.ylabel("Number of samples")
plt.tight_layout()
plt.savefig("mpox.consensus_length.pdf")


df["over20_total"] = df["last_20X"] - df["first_20X"] + 1
df_with_cons = df.loc[df["consensus_length"].notna()]
spearman_r, spearman_p = spearmanr(df_with_cons["consensus_length"], df_with_cons["over20_total"])
print("spearman r and p:", spearman_r, spearman_p)


plt.figure(figsize=(4, 4))
min_x = min(df_with_cons["over20_total"])
max_x = max(df_with_cons["over20_total"])
sns.scatterplot(data=df_with_cons, x="over20_total", y="consensus_length")
plt.plot([min_x, max_x], [min_x, max_x], color="gray")
plt.xlabel("Approximate expected length")
plt.ylabel("Viridian consensus length")
plt.tight_layout()
plt.savefig("mpox.scatter_lengths.pdf")


max_amp = 163
amp_fail_counts = [0] * max_amp
for i, d in df.iterrows():
    if d["viridian_result"] != "Success" or pd.isna(d["dropped_amplicons"]):
        continue

    for x in str(d["dropped_amplicons"]).split(","):
        amp_fail_counts[int(x)-1] += 1


red_bars = {75, 118, 11, 26, 28, 56, 59, 60, 74, 96}
colours = ["red" if x in red_bars else "blue" for x in range(1, max_amp+1, 1)]

fig, ax = plt.subplots(figsize=(6, 2))
ax.bar(list(range(1, max_amp+1, 1)), amp_fail_counts, color=colours)
ax.set_xlabel("Amplicon number")
ax.set_ylabel("Failed samples")
plt.tight_layout()
plt.savefig("mpox.dropped_amps.pdf")
