#!/usr/bin/env python3

import argparse
import csv
import json
import gzip
import os
import subprocess
import textwrap

import matplotlib


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt



vdn_pass_in_gb_colour = "skyblue"
vdn_pass_not_in_gb_colour = "paleturquoise"
vdn_fail_colour = "lightgray"

vdn_pass_colour = "skyblue"
vdn_fail_colour = "darksalmon"

in_tree_colour = "#386cb0"
qc_fail_colour = "darksalmon"
new_colour = "#fdc086"
SEA_COLOUR = "aliceblue"
LAND_COLOUR = "#B2D1B2"
BORDER_COLOUR = "white"


in_tree_colour = "#33a02c"
new_colour = "#1f78b4"
SEA_COLOUR = "aliceblue"
LAND_COLOUR = "lightgray"
LAND_COLOUR = "#bdbdbd"
BORDER_COLOUR = "white"



COUNTRY_COORDS = {
    "Angola": (230, 185),
    "Argentina": (136, 212),
    "Australia": (375, 200),
    "Austria": (210, 222),
    "Bangladesh": (318, 140),
    "Belgium": (162, 202),
    "Bermuda": (140, 134),
    "Botswana": None,
    "Brazil": (152, 187),
    "Cameroon": (228, 162),
    "Canada": (88, 102),
    "Chile": (125, 206),
    "China": (334, 128),
    "Costa Rica": (110, 158),
    "Denmark": (189, 160),
    "Ecuador": (120, 170),
    "Egypt": (250, 138),
    "Estonia": (258, 135),
    "Ethiopia": (260, 160),
    "Europe": (230, 110),
    "Finland": (260, 100),
    "France": (160, 230),
    "Germany": (192, 193),
    "Ghana": (210, 160),
    "Greece": (250, 280),
    "Hong Kong": (350, 145),
    "India": (305, 145),
    "Iraq": (268, 132),
    "Ireland": (112, 185),
    "Israel": (240, 122),
    "Italy": (205,  255),
    "Japan": (380,126),
    "Jordan": (265, 145),
    "Kenya": None,
    "Latvia": (255, 155),
    "Lebanon": (253, 120),
    "Malawi": (252, 184),
    "Mauritius": (290, 195),
    "Mexico": (88, 146),
    "Mozambique": (265,210),
    "Namibia": (228, 198),
    "Netherlands": (170, 182),
    "Northern Mariana Islands": (385, 160),
    "Norway": (187, 127),
    "Pakistan": (293, 133),
    "Portugal": (110,273),
    "Qatar": (282, 125),
    "Russia": (325, 150),
    "Rwanda": (275, 172),
    "Senegal": (190, 150),
    "Seychelles": None,
    "Singapore": None,
    "Slovakia": (235, 215),
    "Slovenia": (230, 240),
    "South Africa": (241, 212),
    "Spain": (132, 266),
    "Sri Lanka": (311, 161),
    "Sweden": None,
    "Switzerland": (185, 230),
    "Thailand": (332, 150),
    "Uganda": (248, 165),
    "United Kingdom": (140, 187),
    "Uruguay": None,
    "USA": (88, 124),
    "Viet Nam": (350, 159),
    "Zimbabwe": (247,200),
}


EUROPE_COUNTRIES = {
    "Austria",
    "Belgium",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Ireland",
    "Italy",
    "Latvia",
    "Netherlands",
    "Norway",
    "Portugal",
    "Russia",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "Switzerland",
    "United Kingdom",
}


LABEL_BELOW = {
    "Argentina",
    "Belgium",
    "Ecuador",
    "Ethiopia",
    "Egypt",
    "France",
    "Germany",
    "Italy",
    "Israel",
    "Jordan",
    "Latvia",
    "Mexico",
    "Mozambique",
    "Namibia",
    "Pakistan",
    "Russia",
    "Slovenia",
    "South Africa",
    "Sri Lanka",
    "Swaziland",
    "Switzerland",
    "Thailand",
    "Viet Nam",
}

def load_tsv(infile):
    data = {}
    used_runs = set()

    with gzip.open(infile, "rt") as f:
        init_keys = ["total", "processed", "in_tree", "new"]
        for d in csv.DictReader(f, delimiter="\t"):
            used_runs.add(d["Run"])
            country = d["Country"]
            if country in  ["NOT_FOUND", "missing"]:
                country = "UNKNOWN"
            if country not in data:
                data[country] = {x: 0 for x in init_keys}

            dc = data[country]
            dc["total"] += 1
            dc["processed"] += 1
            if d["In_Viridian_tree"] == "T":
                dc["in_tree"] += 1


    print("Total countries", len(data))
    print("Countries >= 10 samples", len([d for d in data.values() if d["total"] >=10]))
    print("Countries >= 100 samples", len([d for d in data.values() if d["total"] >=100]))
    print("Countries >= 100 samples in viridian tree", len([d for d in data.values() if d["in_tree"] >=100]))

    return data, used_runs


def add_new_data_to_country_counts(used_runs, country_data):
    init_keys = ["total", "processed", "in_tree", "new"]
    new_countries = set()
    with gzip.open("countries.20240319.tsv.gz", "rt") as f:
        for d in csv.DictReader(f, delimiter="\t"):
            if d["run_accession"] in used_runs:
                continue

            country = d["country"].strip().split(":")[0]
            if country == "missing" or len(country) == 0:
                country = "UNKNOWN"


            if country not in country_data:
                new_countries.add(country)
                country_data[country] = {x: 0 for x in init_keys}

            country_data[country]["total"] += 1
            country_data[country]["new"] += 1

    for x in new_countries:
        print("New country", x, country_data[x]["new"])




def svg2pdf(svg, pdf):
    subprocess.check_output(f"inkscape {svg} --export-type pdf -o {pdf}", shell=True)


def make_map_no_donuts(outfile, europe=False):
    if europe:
        world_map = Basemap(llcrnrlon=-12, llcrnrlat=36, urcrnrlon=45, urcrnrlat=70, resolution='i', projection="merc")
    else:
        world_map = Basemap(llcrnrlon=-140, llcrnrlat=-60,urcrnrlon=160,urcrnrlat=70)
    world_map.drawmapboundary(fill_color=SEA_COLOUR, linewidth=0)
    world_map.fillcontinents(color=LAND_COLOUR, lake_color=SEA_COLOUR)
    world_map.drawcountries(color=BORDER_COLOUR, linewidth=0.1)
    #fig = plt.figure()
    #fig.tight_layout()
    plt.savefig(outfile)
    plt.close()



def donut_plot(values, outfile, country):
    #colours = [vdn_pass_in_gb_colour, vdn_pass_not_in_gb_colour, vdn_fail_colour]
    #colours = [in_tree_colour, qc_fail_colour, new_colour]
    colours = [in_tree_colour, new_colour]
    fig = plt.figure(figsize=(5,5))
    circle = plt.Circle((0,0), 0.7, color='white', linewidth=0, alpha=0.8)
    plt.pie(values, colors=colours, counterclock=False, startangle=90, wedgeprops = {"linewidth": 0})
    plt.text(0, 0, str(sum(values)), horizontalalignment='center', verticalalignment='center', fontsize=50)

    if country in LABEL_BELOW:
        y_text = -1.01
        valign = 'top'
    else:
        y_text = 1.01
        valign = 'bottom'

    country_replace = {
        "Uganda": "Uganda  ",
        "United Kingdom": "UK",
        "Northern Mariana Islands": "N. Mariana Isl",
    }

    country = country_replace.get(country, country)
    plt.text(0, y_text, country, horizontalalignment='center', verticalalignment=valign, fontsize=50)

    p=plt.gcf()
    p.gca().add_artist(circle)
    plt.savefig(outfile, transparent=True)
    plt.close()


def make_counts(all_counts):
    '''all_counts should be counts dictionary made by samples_table.make_samples_tsv()'''
    europe_counts = {x: all_counts[x] for x in all_counts if x in EUROPE_COUNTRIES}
    world_counts = {x: all_counts[x] for x in all_counts if x not in EUROPE_COUNTRIES}
    #keys = ["in_tree", "qc_fail", "new"]
    keys = ["in_tree", "new"]
    world_counts["Europe"] = {k: 0 for k in keys}
    for x in europe_counts:
        for k in world_counts['Europe']:
            world_counts['Europe'][k] += europe_counts[x][k]

    return world_counts, europe_counts


def make_donuts(counts_dict, outprefix):
    files = {}
    for country in counts_dict:
        outfile = f'{outprefix}.{country}.svg'.replace(' ', '_')
        files[country] = outfile
        if os.path.exists(outfile):
            continue
        #values = [counts_dict[country][x] for x in ["in_tree", "qc_fail", "new"]]
        #values = [values[0], values[1], values[2]]
        values = [counts_dict[country][x] for x in ["in_tree", "new"]]
        values = [values[0], values[1]]
        donut_plot(values, outfile, country)

    return files


def make_map_with_donuts(counts, outprefix, europe=False, debug=False):
    no_donuts_svg = f'{outprefix}.tmp.svg'
    final_svg = f'{outprefix}.svg'
    final_pdf = final_svg.replace('.svg', '.pdf')
    donut_files = make_donuts(counts, outprefix)
    make_map_no_donuts(no_donuts_svg, europe=europe)
    donut_size = 32 if europe else 21

    with open(no_donuts_svg) as f:
        svg_lines = [x.rstrip() for x in f]
    assert svg_lines[-1] == '</svg>'
    last_svg_line = svg_lines.pop()

    # lines to point to various smaller countries
    if europe:
        # Slovenia
        svg_lines.append('<line x1="240" y1="255" x2="228" y2="250" style="stroke:rgb(100,100,100);stroke-width:0.5" />')
    else:
        # Mozambique
        #svg_lines.append('<line x1="275" y1="230" x2="268" y2="202" style="stroke:rgb(0,0,0);stroke-width:0.5" />')
        svg_lines.append('<line x1="268" y1="202" x2="275" y2="220" style="stroke:rgb(100,100,100);stroke-width:0.5" />')
        # Rwanda
        svg_lines.append('<line x1="260" y1="184" x2="285" y2="180" style="stroke:rgb(100,100,100);stroke-width:0.5" />')
        # Israel
        svg_lines.append('<line x1="250" y1="134" x2="265" y2="143" style="stroke:rgb(100,100,100);stroke-width:0.5" />')
        # Jordan
        svg_lines.append('<line x1="275" y1="150" x2="267" y2="143" style="stroke:rgb(100,100,100);stroke-width:0.5" />')
        # Lebanon
        svg_lines.append('<line x1="263" y1="135" x2="267" y2="140" style="stroke:rgb(100,100,100);stroke-width:0.5" />')
        # Qatar
        #svg_lines.append('<line x1="294" y1="140" x2="285" y2="150" style="stroke:rgb(100,100,100);stroke-width:0.5" />')
        # Viet Nam
        svg_lines.append('<line x1="350" y1="155" x2="360" y2="170" style="stroke:rgb(100,100,100);stroke-width:0.5" />')

    for country in donut_files:
        if country not in COUNTRY_COORDS or COUNTRY_COORDS[country] is None:
            print("Fix country:", country)
            continue
        x, y = COUNTRY_COORDS[country]
        filename = os.path.abspath(donut_files[country])
        svg_lines.append(f'<image x="{x}" y="{y}" width="{donut_size}" height="{donut_size}" xlink:href="file:{filename}"></image>')


    svg_lines.append(last_svg_line)
    with open(final_svg, 'w') as f:
        print(*svg_lines, sep='\n', file=f)

    svg2pdf(final_svg, final_pdf)

    if not debug:
        os.unlink(no_donuts_svg)
        os.unlink(final_svg)
        for filename in donut_files.values():
            os.unlink(filename)


def make_legend(outprefix, debug=False):
    svg_file = f'{outprefix}.svg'
    pdf_file = f'{outprefix}.pdf'
    s = r'''        <svg height="70pt" width="180pt">
        <text x="10" y="11">Sample status</text>
        <circle cx="11" cy="30" r="10" stroke="black" stroke-width="0.5" fill="''' + in_tree_colour + r'''" />
        <text x="23" y="35">In Viridian tree</text>
        <circle cx="11" cy="55" r="10" stroke="black" stroke-width="0.5" fill="''' + new_colour + r'''" />
        <text x="23" y="60">New</text>
        </svg>'''

    with open(svg_file, 'w') as f:
        print(textwrap.dedent(s), file=f)

    svg2pdf(svg_file, pdf_file)
    if not debug:
        os.unlink(svg_file)



parser = argparse.ArgumentParser(
    description = "Make map figure for viridian paper",
    usage="%(prog)s <run_tsv_gz> <outprefix>",
)

parser.add_argument(
    "run_tsv_gz",
    help="gzipped TSV file of run data",
)
parser.add_argument(
    "outprefix",
    help="Prefix of output files",
)
options = parser.parse_args()



country_data, used_runs = load_tsv(options.run_tsv_gz)
print("Loaded TSV file", options.run_tsv_gz, flush=True)

add_new_data_to_country_counts(used_runs, country_data)
print("Added new runs to country counts", flush=True)


with open(f"{options.outprefix}.suppl_counts.tsv", "w") as f:
    print("Country", "total", "processed", "in_tree", "new", sep="\t", file=f)
    for c, d in sorted(country_data.items()):
        print(c, d["total"], d["processed"], d["in_tree"], d["new"], sep="\t", file=f)

to_ignore = {"UNKNOWN"}
for c, d in sorted(country_data.items()):
    d["qc_fail"] = int(d["processed"]) - int(d["in_tree"])
    if d["in_tree"] + d["new"] < 100:
        to_ignore.add(c)
        print("Ignoring country", c, d)

country_data = {k: d for k, d in country_data.items() if k not in to_ignore}

print("Make map", flush=True)

debug = False
world_outprefix = f"{options.outprefix}.world"
europe_outprefix = f"{options.outprefix}.europe"
make_legend(f"{options.outprefix}.legend", debug=debug)
world_counts, europe_counts = make_counts(country_data)
make_map_with_donuts(world_counts, world_outprefix, europe=False, debug=debug)
make_map_with_donuts(europe_counts, europe_outprefix, europe=True, debug=debug)

