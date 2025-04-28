#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data.tsv.gz", delimiter="\t")
plt.figure(figsize=(8, 4))
sns.lineplot(data=df, x="Position", y="Viridian", label="Viridian")
sns.lineplot(data=df, x="Position", y="GenBank", label="GenBank")
plt.xlabel("Genome Position")
plt.ylabel("Number of samples")
plt.legend()
plt.tight_layout()
plt.savefig("plot.pdf")
