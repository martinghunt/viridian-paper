#!/usr/bin/env python3

import copy
import csv
import statistics
from matplotlib import pyplot as plt


def print_averages(data_lists, prefix):
    tool_all_tech = {}
    for tech in data_lists:
        for tool, vals in data_lists[tech].items():
            if tool not in tool_all_tech:
                tool_all_tech[tool] = []
            tool_all_tech[tool].extend(vals)
            print(
                prefix,
                tech,
                tool,
                "median=" + str(round(statistics.median(vals), 3)),
                "mean=" + str(round(statistics.mean(vals), 3)),
                sep="\t",
            )
    for tool, vals in tool_all_tech.items():
        print(
            prefix,
            "All",
            tool,
            "median=" + str(round(statistics.median(vals), 3)),
            "mean=" + str(round(statistics.mean(vals), 3)),
            sep="\t",
        )

plt.style.use("grayscale")
TOOLS = ["ARTIC-ILM", "ARTIC-ONT", "Viridian"]

ram = {
    "Nanopore": {"ARTIC-ONT": [], "Viridian": []},
    "Illumina": {"ARTIC-ILM": [], "Viridian": []},
}

wall_clock = copy.deepcopy(ram)
cpu = copy.deepcopy(ram)


with open("run_time_ram_suppl.tsv") as f:
    for d in csv.DictReader(f, delimiter="\t"):
        if d["Amplicon_scheme"] == "sispa":
            continue

        ilm_ont = "ILM" if d["Platform"] == "Illumina" else "ONT"
        ram[d["Platform"]][f"ARTIC-{ilm_ont}"].append(float(d[f"ARTIC-{ilm_ont}_ram"]))
        ram[d["Platform"]]["Viridian"].append(float(d["Viridian_ram"]))
        cpu[d["Platform"]][f"ARTIC-{ilm_ont}"].append(float(d[f"ARTIC-{ilm_ont}_cpu"]))
        cpu[d["Platform"]]["Viridian"].append(float(d["Viridian_cpu"]))
        wall_clock[d["Platform"]][f"ARTIC-{ilm_ont}"].append(float(d[f"ARTIC-{ilm_ont}_wall_clock"]))
        wall_clock[d["Platform"]]["Viridian"].append(float(d["Viridian_wall_clock"]))


labels = ["ARTIC-ILM", "Viridian (ILM)", "ARTIC-ONT", "Viridian (ONT)"]

data_lists = [
    ram["Illumina"]["ARTIC-ILM"],
    ram["Illumina"]["Viridian"],
    ram["Nanopore"]["ARTIC-ONT"],
    ram["Nanopore"]["Viridian"],
]

print_averages(ram, "ram")


fig, ax = plt.subplots(figsize=(8,3))
ax.boxplot(data_lists, vert=True, labels=labels)
plt.ylabel("Peak RAM (GB)")
plt.tight_layout()
plt.savefig("ram.pdf")
plt.clf()


data_lists = [
    wall_clock["Illumina"]["ARTIC-ILM"],
    wall_clock["Illumina"]["Viridian"],
    wall_clock["Nanopore"]["ARTIC-ONT"],
    wall_clock["Nanopore"]["Viridian"],
]

print_averages(wall_clock, "wall_clock")

fig, ax = plt.subplots(figsize=(8,3))
ax.boxplot(data_lists, vert=True, labels=labels)
plt.ylabel("Wall clock (s)")
plt.tight_layout()
plt.savefig("wall_clock.pdf")
plt.clf()

data_lists = [
    cpu["Illumina"]["ARTIC-ILM"],
    cpu["Illumina"]["Viridian"],
    cpu["Nanopore"]["ARTIC-ONT"],
    cpu["Nanopore"]["Viridian"],
]


print_averages(cpu, "cpu")

fig, ax = plt.subplots(figsize=(8,3))
ax.boxplot(data_lists, vert=True, labels=labels)
plt.ylabel("CPU (s)")
plt.tight_layout()
plt.savefig("cpu.pdf")
plt.clf()

