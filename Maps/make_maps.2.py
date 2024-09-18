#!/usr/bin/env python3

import argparse
import csv
import json
import gzip
import os
import subprocess


COUNTRY_COORDS = {
    "Angola": (308, 194),
    "Argentina": (178, 241),
    "Australia": (495, 215),
    "Austria": (137, 182),
    "Bangladesh": (428, 134),
    "Belgium": (89, 161),
    "Brazil": (200, 192),
    "Cameroon": (303, 166),
    "Canada": (108, 82),
    "Chile": (165, 224),
    "China": (449, 120),
    "Denmark": (115, 117),
    "Ecuador": (155, 176),
    "Estonia": (191, 94),
    "Europe": (300, 97),
    "Ethiopia": (345, 160),
    "Finland": (196, 60),
    "France": (80, 183),
    "Germany": (117, 162),
    "Ghana": (279, 159),
    "Hong Kong": (462, 141),
    "India": (407, 142),
    "Israel": (318, 125),
    "Italy": (130, 222),
    "Jordan": (344, 144),
    "Latvia": (188, 112),
    "Lebanon": (343, 108),
    "Malawi": (333, 197),
    "Malta": (160, 260),
    "Mauritius": (390, 203),
    "Mexico": (120, 141),
    "Mozambique": (370, 234),
    "Namibia": (298, 213),
    "Netherlands": (92, 143),
    "Norway": (112, 79),
    "Pakistan": (392, 125),
    "Portugal": (27, 245),
    "Qatar": (370, 155),
    "Russia": (250, 105),
    "Rwanda": (360, 193),
    "Senegal": (255, 151),
    "Seychelles": (385, 176),
    "Singapore": (430, 184),
    "Slovakia": (162, 175),
    "South Africa": (323, 230),
    "Spain": (54, 240),
    "Sri Lanka": (412, 164),
    "Switzerland": (108, 190),
    "Thailand": (438, 155),
    "Uganda": (330, 173),
    "USA": (116, 111),
    "United Kingdom": (60, 130),
    "Viet Nam": (480, 166),
    "Zimbabwe": (328, 210),
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
    "Malta",
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


def load_tsv(infile):
    data = {}

    with gzip.open(infile, "rt") as f:
        for d in csv.DictReader(f, delimiter="\t"):
            if d["In_Viridian_tree"] != "T" or d["Country"] == "UNKNOWN":
                continue
            data[d["Country"]] = data.get(d["Country"], 0) + 1

    print("Total countries", len(data))
    print("Countries >= 50 samples", len([v for v in data.values() if v >= 50]))
    print("Countries >= 100 samples", len([v for v in data.values() if v >= 100]))
    return data


def svg2pdf(svg, pdf):
    subprocess.check_output(f"inkscape {svg} --export-type pdf -o {pdf}", shell=True)


def make_counts(all_counts):
    """all_counts should be counts dictionary made by samples_table.make_samples_tsv()"""
    europe_counts = {x: all_counts[x] for x in all_counts if x in EUROPE_COUNTRIES}
    world_counts = {x: all_counts[x] for x in all_counts if x not in EUROPE_COUNTRIES}
    world_counts["Europe"] = sum(europe_counts.values())
    return world_counts, europe_counts


def make_map_with_labels(counts, outprefix, counts_file, europe=False):
    area = "europe" if europe else "world"
    no_labels_svg = f"{outprefix}.tmp.svg"
    command = f"./make_maps.2.R {counts_file} {area} {no_labels_svg}"
    subprocess.check_output(command.split())
    final_svg = f"{outprefix}.svg"
    final_pdf = final_svg.replace(".svg", ".pdf")

    with open(no_labels_svg) as f:
        svg_lines = [x.rstrip() for x in f]
    os.unlink(no_labels_svg)
    assert svg_lines[-1] == "</svg>"
    last_svg_line = svg_lines.pop()

    # lines to point to various smaller countries
    if europe:
        pass
        # Malta
        svg_lines.append(
            '<line x1="151" y1="263" x2="140" y2="274" style="stroke:rgb(100,100,100);stroke-width:0.5" />'
        )
    else:
        # Mozambique
        svg_lines.append(
            '<line x1="353" y1="227" x2="344" y2="202" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Rwanda
        svg_lines.append(
            '<line x1="346" y1="191" x2="330" y2="181" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Israel
        svg_lines.append(
            '<line x1="327" y1="125" x2="336" y2="126" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Jordan
        svg_lines.append(
            '<line x1="345" y1="138" x2="340" y2="128" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Lebanon
        svg_lines.append(
            '<line x1="333" y1="110" x2="338" y2="123" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Viet Nam
        svg_lines.append(
            '<line x1="470" y1="160" x2="454" y2="152" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Mauritius
        svg_lines.append(
            '<line x1="376" y1="205" x2="372" y2="209" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Singapore
        svg_lines.append(
            '<line x1="438" y1="180" x2="447" y2="175" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Qatar
        svg_lines.append(
            '<line x1="371" y1="150" x2="363" y2="137" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )
        # Seychelles
        svg_lines.append(
            '<line x1="371" y1="184" x2="375" y2="179" style="stroke:rgb(0,0,0);stroke-width:0.5" />'
        )

    font_size = 'font-size="1ex"'

    for country, count in counts.items():
        if country not in COUNTRY_COORDS or COUNTRY_COORDS[country] is None:
            print("Fix country:", country)
            continue
        x, y = COUNTRY_COORDS[country]
        svg_lines.append(
            f'<text text-anchor="middle" {font_size} x="{x}" y="{y}">{country}</text>'
        )
        svg_lines.append(
            f'<text text-anchor="middle" {font_size} x="{x}" y="{y+7}">{count}</text>'
        )

    svg_lines.append(last_svg_line)
    with open(final_svg, "w") as f:
        print(*svg_lines, sep="\n", file=f)

    svg2pdf(final_svg, final_pdf)


parser = argparse.ArgumentParser(
    description="Make map figure for viridian paper",
    usage="%(prog)s <metadata_tsv_gz> <outprefix>",
)

parser.add_argument(
    "metadata_tsv_gz",
    help="gzipped TSV file of metadata",
)
parser.add_argument(
    "outprefix",
    help="Prefix of output files",
)
options = parser.parse_args()


country_counts = load_tsv(options.metadata_tsv_gz)
print("Loaded TSV file", options.metadata_tsv_gz, flush=True)

# to copy into supplementary spreadsheet
with open(f"{options.outprefix}.suppl_counts.tsv", "w") as f:
    print("name\tcount", file=f)
    for k, v in sorted(country_counts.items()):
        print(k, v, sep="\t", file=f)

country_counts = {k: v for k, v in country_counts.items() if v >= 50}


world_outprefix = f"{options.outprefix}.world"
europe_outprefix = f"{options.outprefix}.europe"
world_counts, europe_counts = make_counts(country_counts)
print("world_counts:", world_counts)
print("europe _counts:", europe_counts)

counts_tsv = f"{options.outprefix}.counts.tsv"
key_replace = {"USA": "United States", "Viet Nam": "Vietnam"}
with open(counts_tsv, "w") as f:
    print("name\tcount", file=f)
    for k, v in country_counts.items():
        print(key_replace.get(k, k), v, sep="\t", file=f)

make_map_with_labels(world_counts, world_outprefix, counts_tsv, europe=False)
make_map_with_labels(europe_counts, europe_outprefix, counts_tsv, europe=True)
os.unlink(counts_tsv)
