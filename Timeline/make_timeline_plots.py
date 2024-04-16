#!/usr/bin/env python3

import csv
import gzip
import matplotlib.pyplot as plt


def gather_data_by_date():
    data = {}
    with gzip.open("maskingStats.2023-07-24.tsv.gz", "rt") as f:
        for line in f:
            name, date, lineage, prob_site, recent_sites_masked = line.rstrip().split(
                "\t"
            )
            if date == "":
                continue
            date_fields = date.split("-")
            if len(date_fields) == 1:
                continue

            assert 2 <= len(date_fields) <= 3
            year = date_fields[0]
            month = date_fields[1]

            assert len(year) == 4
            if not 2019 <= int(year) <= 2023:
                continue
            assert 2019 <= int(year) <= 2023
            assert 1 <= int(month) <= 12

            date_str = str(year) + str(month).zfill(2)
            assert len(date_str) == 6

            if len(lineage) == 0:
                lineage = "Other"

            if date_str not in data:
                data[date_str] = {}
            data[date_str][lineage] = data[date_str].get(lineage, 0) + 1
    return data


VOCS = {
    "B.1.1.7": "Alpha",
    "B.1.351": "Beta",
    "B.1.617.2": "Delta",
    "BA.1": "BA.1",
    "BA.1.1": "BA.1",
    "BA.2": "BA.2",
    "BA.2.75": "BA.2",
    "BA.4": "Omicron",
    "BA.5": "Omicron",
    "BN.1.2.3": "Other",
    "BQ.1": "Omicron",
    "BQ.1.1": "Omicron",
    "P.1": "Gamma",
    "XBB": "Omicron",
    "XBB.1": "Omicron",
    "XBB.1.5": "Omicron",
    "XBC": "Other",
    "Other": "Other",
}

VOC_COLOURS = {
    "Alpha": "indianred",
    "Beta": "pink",
    "Gamma": "cornflowerblue",
    "Delta": "darkseagreen",
    # "Epsilon": "cornflowerblue",
    # "Iota": "black",
    # "Lambda": "#c6dbef",
    # "Mu": "red",
    "Omicron": "gold",
    # "Omicron_probable": "goldenrod",
    # "Zeta": "red",
    # "Theta": "#ce1256",
    # "Eta": "#91003f",
    "Other": "lightblue",
    "BA.1": "orange",
    "BA.2": "darkorange",
}


data_by_date = gather_data_by_date()
all_variants = set()

voc_data = {}
for date in data_by_date:
    new_d = {}
    for k, v in data_by_date[date].items():
        new_k = VOCS[k]
        new_d[new_k] = new_d.get(new_k, 0) + v
        all_variants.add(new_k)
    year = int(date[:4])
    month = int(date[-2:])
    voc_data[(year, month)] = new_d

months = sorted(list(voc_data.keys()))
month2xval = {m: i for i, m in enumerate(months)}
voc_names = sorted(list(all_variants))
month_x_vals = list(month2xval.values())


mask_x_vals = []
mask_site_counts = []
mask_node_counts = []
month2days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
with gzip.open("BSM_sites_nodes.tsv.gz", "rt") as f:
    for d in csv.DictReader(f, delimiter="\t"):
        year, month, day = d["date"].split("-")
        year = int(year)
        month = int(month)
        day = int(day)
        assert 1 <= month <= 12
        if not months[0] <= (year, month) <= months[-1]:
            break
        days_in_month = month2days[month - 1]
        assert 1 <= day <= days_in_month
        x_val = month2xval[(year, month)]
        x_val += day / days_in_month
        mask_x_vals.append(x_val)
        mask_site_counts.append(int(d["site_count"]))
        mask_node_counts.append(int(d["node_count"]))


voc_data_lists = {x: [] for x in all_variants}

for month in months:
    for voc in voc_names:
        voc_data_lists[voc].append(voc_data[month].get(voc, 0) / 1_000_000)

x_tick_pos = []
x_tick_labels = []
for i, month in enumerate(months):
    if i % 4 != 0:
        continue
    x_tick_pos.append(month_x_vals[i])
    x_tick_labels.append(f"{month[0]}-{str(month[1]).zfill(2)}")

y_lists = [voc_data_lists[x] for x in voc_names]
y_lists_pc = [[] for _ in range(len(y_lists))]


for j in range(len(y_lists[0])):
    total = sum(y_lists[i][j] for i in range(len(y_lists)))
    for i in range(len(y_lists)):
        y_lists_pc[i].append(100 * y_lists[i][j] / total)


PERCENT = False

colormap = [VOC_COLOURS[x] for x in voc_names]

f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 5), sharex=True)

ax2.plot(mask_x_vals, mask_site_counts)
ax2.set_ylabel("Masked sites")
ax3.plot(mask_x_vals, mask_node_counts)
ax3.set_ylabel("Masked nodes")


if PERCENT:
    ax1.stackplot(month_x_vals, y_lists_pc, labels=voc_names, colors=colormap)
else:
    ax1.stackplot(month_x_vals, y_lists, labels=voc_names, colors=colormap)

ax1.legend(loc="upper right",  prop={'size': 6})
plt.xticks(x_tick_pos, x_tick_labels, rotation=45, horizontalalignment="right")
ax3.set_xlabel("Date")
if PERCENT:
    ax1.set_ylabel("Percent of samples")
    out = "timeline.suppl.pdf"
else:
    ax1.set_ylabel("Samples ($10^6$)")
    out = "timeline.suppl.pdf"
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(out)

plt.clf()
plt.close()


artic_dates = [
    (2020, 1, 22),  # artic 1
    (2020, 4, 9),  #  2
    (2020, 8, 25),  # 3
    (2021, 6, 2),  #  4
    (2021, 12, 1),  # 4.1
    (2023, 1, 5),  #  5.3.2
]
artic_x = [
    month2xval[(t[0], t[1])] + (t[2] / month2days[t[1] - 1]) for t in artic_dates
]


plt.figure(figsize=(10, 4))

if PERCENT:
    plt.stackplot(month_x_vals, y_lists_pc, labels=voc_names, colors=colormap)
else:
    plt.stackplot(month_x_vals, y_lists, labels=voc_names, colors=colormap)

plt.xticks(x_tick_pos, x_tick_labels, rotation=45, horizontalalignment="right")
if PERCENT:
    plt.label("Percent of samples", fontsize=16)
    out = "timeline.main.pdf"
else:
    plt.ylabel("Number of samples ($10^6$)", fontsize=15)
    out = "timeline.main.pdf"

artic_opts = {"marker": "v", "color": "#40826D", "edgecolors": "black", "s": 140}
plt.scatter(artic_x, [0.03] * len(artic_x), **artic_opts)
plt.scatter(0, 0.28, **artic_opts)  # for legend
plt.text(0.6, 0.26, "ARTIC updates")
plt.xlabel("Date", fontsize=16)
ax = plt.subplot()
plt.legend(loc="upper right", frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)


annot_opts = {"xycoords": "data", "textcoords": "offset points", "size": 14}
arrow_opts = {"arrowstyle": "fancy", "facecolor": "lightgrey", "edgecolor": "black"}

label_data = [
    # https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0239403
    ("a", (2020, 9, 18), (-20, 50), -20, -110),
    # https://virological.org/t/recent-evolution-and-international-transmission-of-sars-cov-2-clade-19b-pango-a-lineages/711
    ("b", (2021, 6, 1), (-80, 90), 70, -20),
    # https://wellcomeopenresearch.org/articles/6-305/v1
    # also preprint is https://www.medrxiv.org/content/10.1101/2021.10.14.21264847v1.article-info, dated 2021/10/21
    ("c", (2021, 10, 21), (-100, 120), 20, -70),
    # https://virological.org/t/issues-with-sars-cov-2-sequencing-data/473/16
    ("d", (2021, 11, 1), (-30, 180), 0, 90),
    # https://community.artic.network/t/sars-cov-2-v4-1-update-for-omicron-variant/342
    ("e", (2021, 12, 1), (70, 150), 75, 0),
]

for label, date, xytext, angleA, angleB in label_data:
    x = month2xval[date[:2]] + (date[2] / month2days[date[1] - 1])

    ax.annotate(
        label,
        xy=(x, 0),
        xytext=xytext,
        **annot_opts,
        arrowprops=dict(
            **arrow_opts,
            connectionstyle=f"angle3,angleA={angleA},angleB={angleB}",
        ),
    )

plt.tight_layout()
plt.savefig(out)
plt.savefig(out.replace(".pdf", ".png"), dpi=600)
