"""
process_file.py — Part 2: one file of package descriptions, uploaded.

A Streamlit app that accepts an uploaded text file with one package description
per line, shows the total for every line, and writes the parsed packages to a
JSON file in the `data/` folder — `data/packaging1.txt` in, `data/packaging1.json`
out.

New here: an uploaded file arrives as **bytes**, not text, so it has to be
decoded before it can be split into lines. And a text file usually ends with a
newline, so the last "line" is empty and must be skipped rather than parsed.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_file
"""

# --- The page ---------------------------------------------------------------------
#
# Less scaffolding this time. The steps are described, but which widget and which
# function does each job — and what to call the result — is now yours to work out.
# `one_package.py` is your worked example for anything structural, and README
# Reference #4 and #5 cover the two things that are new here.

import json

import streamlit as st

from packaging_parser import calc_total_units, get_unit, parse_packaging


st.title("Process File of Packages")

package_file = st.file_uploader("Upload a package file", key="package_file")

if package_file is not None:
    text = package_file.getvalue().decode("utf-8")
    lines = text.splitlines()
    packages = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        package = parse_packaging(line)
        total = calc_total_units(package)
        unit = get_unit(package)

        st.info(f"{line} ➡️ Total 📦 Size: {total} {unit}")
        packages.append(package)

    json_name = package_file.name.replace(".txt", ".json")
    with open(f"data/{json_name}", "w", encoding="utf-8") as fh:
        json.dump(packages, fh)

    st.success(f"{len(packages)} packages written to data/{json_name}")
