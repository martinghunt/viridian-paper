#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys

import matplotlib.pyplot as plt

set1_cmap = plt.get_cmap("Set1")


COLOURS = {
    "COVID-ARTIC-V3": set1_cmap(0),
    "COVID-ARTIC-V4.1": set1_cmap(1),
    "COVID-ARTIC-V5.0-5.3.2_400": set1_cmap(2),
    "COVID-ARTIC-V5.0-5.2.0_1200": set1_cmap(3),
    "COVID-MIDNIGHT-1200": set1_cmap(4),
    "COVID-AMPLISEQ-V1": set1_cmap(6),
    "COVID-VARSKIP-V1a-2b": set1_cmap(7),
    "wgs": "gray",
}

def run_one_sim(vdn_container, outdir, read_length, debug=False):
    command = f"singularity exec {vdn_container} viridian sim_schemes --outdir {outdir} --read_length {read_length}"
    if debug:
        command += " --debug"
    print(command, file=sys.stderr)
    subprocess.check_output(command, shell=True)
    with open(f"{outdir}/summary.json") as f:
        results = json.load(f)

    return results



parser = argparse.ArgumentParser(
    description="run simulations to evaluate viridian scores for amplicon schemes",
    usage="%(prog)s [options] <viridian container> <outprefix>",
)
parser.add_argument("--debug", action="store_true", help="Debug mode, do not clean temp files")
parser.add_argument("viridian_container", help="Filename of singularity viridian container file")
parser.add_argument("outprefix", help="Prefix of output files")
options = parser.parse_args()

read_lengths = [100, 120, 140, 160, 180, 200, 250, 300, 400, 500, 750, 1000, 1250, 1500, 2000]
sims_dir = options.outprefix + ".tmp.sims"
os.mkdir(sims_dir)
results = {l: run_one_sim(options.viridian_container, f"{sims_dir}/sim.{l}", l, debug=options.debug) for l in read_lengths}
with open(f"{options.outprefix}.results.json", "w") as f:
    json.dump(results, f, indent=2)

#with open(f"{options.outprefix}.results.json") as f:
#    results = json.load(f)
#results = {int(k): v for k, v in results.items()}

with open(f"{options.outprefix}.suppl_table.tsv", "w") as f:
    print("Fragment_length", "Scheme", "Truth_score", "Best_score", "Second_best_score", "Score_ratio", "Correct_call", "Pass_QC", sep="\t", file=f)
    for frag_len in results:
        for scheme, d in results[frag_len].items():
            if "full_length" in scheme:
                continue
            scheme = scheme.split(":")[0]
            second_score = sorted(list(d["scores"].values()))[-2]
            score_ratio = second_score / d["best_score"]

            if scheme == "wgs":
                truth_score = "NA"
                correct_call = "NA"
            else:
                truth_score = d["scores"][scheme]
                correct_call = scheme == d["best_scheme"]
            pass_filter = (score_ratio < 0.5 and d["best_score"] > 250)

            print(
                frag_len,
                scheme,
                truth_score,
                d["best_score"],
                second_score,
                score_ratio,
                correct_call,
                pass_filter,
                sep="\t",
                file=f,
            )




for l in read_lengths:
    results[l] = {k.replace(":fragmented", ""): v for k, v in results[l].items() if k.endswith(":fragmented") or k=="wgs"}

assert set(COLOURS.keys()) == set(results[read_lengths[0]].keys())
markers = {True: "o", False: "x"}

for use_actual in [True, False]:
    for scheme in COLOURS:
        x_vals = read_lengths
        if scheme == "wgs":
            check = "na"
            y_vals = [results[l][scheme]["best_score"] for l in read_lengths]
        else:
            check = [results[l][scheme]["best_scheme"] == scheme for l in read_lengths]
            if use_actual:
                y_vals = [results[l][scheme]["scores"][scheme] for l in read_lengths]
            else:
                y_vals = [results[l][scheme]["best_score"] for l in read_lengths]
            for tf in markers:
                tmp_x_vals = [x for i, x in enumerate(read_lengths) if check[i] == tf]
                tmp_y_vals = [y for i, y in enumerate(y_vals) if check[i] == tf]
                plt.scatter(tmp_x_vals, tmp_y_vals, color=COLOURS[scheme], marker=markers[tf], s=15)
        plt.plot(x_vals, y_vals, color=COLOURS[scheme], label=scheme)
        if use_actual:
            plt.legend(title="Scheme")

    plt.xlabel("Fragment length")
    plt.axhline(250, linestyle='--', color="lightgray")
    if use_actual:
        plt.ylabel("Score of truth scheme")
    else:
        plt.ylabel("Score of best scheme")
    plt.tight_layout()
    if use_actual:
        plt.savefig(f"{options.outprefix}.best_score_actual.pdf")
    else:
        plt.savefig(f"{options.outprefix}.best_score.pdf")
    plt.clf()

    for scheme in COLOURS:
        y_vals = [results[l][scheme]["score_ratio"] for l in read_lengths]
        if scheme == "wgs":
            check = "na"
            x_vals = [results[l][scheme]["best_score"] for l in read_lengths]
        else:
            check = [results[l][scheme]["best_scheme"] == scheme for l in read_lengths]
            if use_actual:
                x_vals = [results[l][scheme]["scores"][scheme] for l in read_lengths]
            else:
                x_vals = [results[l][scheme]["best_score"] for l in read_lengths]

            for tf in markers:
                tmp_x_vals = [x for i, x in enumerate(x_vals) if check[i] == tf]
                tmp_y_vals = [y for i, y in enumerate(y_vals) if check[i] == tf]
                plt.scatter(tmp_x_vals, tmp_y_vals, color=COLOURS[scheme], marker=markers[tf], s=15)
        plt.plot(x_vals, y_vals, color=COLOURS[scheme], label=scheme)

    plt.axhline(0.5, color="lightgray", linestyle="--", linewidth=1)
    plt.axvline(250, color="lightgray", linestyle="--", linewidth=1)
    plt.ylabel("Second best score / best score")
    if use_actual:
        plt.xlabel("Score of truth scheme")
    else:
        plt.xlabel("Score of best scheme")
    plt.tight_layout()
    if use_actual:
        plt.savefig(f"{options.outprefix}.scatter_actual_score_v_ratio.pdf")
    else:
        plt.savefig(f"{options.outprefix}.scatter_score_v_ratio.pdf")
    plt.clf()


for scheme in COLOURS:
    x_vals = read_lengths
    if scheme == "wgs":
        check = "na"
        y_vals = [results[l][scheme]["score_ratio"] for l in read_lengths]
    else:
        check = [results[l][scheme]["best_scheme"] == scheme for l in read_lengths]
        y_vals = [results[l][scheme]["score_ratio"] for l in read_lengths]
        for tf in markers:
            tmp_x_vals = [x for i, x in enumerate(read_lengths) if check[i] == tf]
            tmp_y_vals = [y for i, y in enumerate(y_vals) if check[i] == tf]
            plt.scatter(tmp_x_vals, tmp_y_vals, color=COLOURS[scheme], marker=markers[tf], s=15)

    plt.plot(x_vals, y_vals, color=COLOURS[scheme], label=scheme)

plt.xlabel("Fragment length")
plt.ylabel("Second best score / Best score")
plt.axhline(0.5, linestyle='--', color="lightgray")
plt.tight_layout()
plt.savefig(f"{options.outprefix}.score_ratio.pdf")
plt.clf()


max_x = 0
max_y = 0
for scheme in COLOURS:
    if scheme == "wgs":
        check = "na"
        x_vals = [results[l][scheme]["best_score"] for l in read_lengths]
        y_vals = [sorted(list(results[l][scheme]["scores"].values()))[-2] for l in read_lengths]
    else:
        check = [results[l][scheme]["best_scheme"] == scheme for l in read_lengths]
        x_vals = [results[l][scheme]["best_score"] for l in read_lengths]
        y_vals = [sorted(list(results[l][scheme]["scores"].values()))[-2] for l in read_lengths]
        for tf in markers:
            tmp_x_vals = [x for i, x in enumerate(x_vals) if check[i] == tf]
            tmp_y_vals = [y for i, y in enumerate(y_vals) if check[i] == tf]
            plt.scatter(tmp_x_vals, tmp_y_vals, color=COLOURS[scheme], marker=markers[tf], s=15)
    max_x = max(max_x, max(x_vals))
    max_y = max(max_y, max(y_vals))
    plt.plot(x_vals, y_vals, color=COLOURS[scheme], label=scheme)

plt.xlabel("Best score")
plt.ylabel("Second best score")
plt.plot([0, max_y], [0, max_y], '--', linewidth=1, color="lightgray")
plt.plot([0, 2*max_y], [0, max_y], '-', linewidth=1, color="lightgray")
plt.tight_layout()
plt.savefig(f"{options.outprefix}.scatter_score_v_second.pdf")
plt.clf()

