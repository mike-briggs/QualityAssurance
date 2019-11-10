# backend.py
# handles all (merged) transactions once a day
import sys
import os
import glob

input_files = glob.glob("*.out.actual.txt")

with open("merge.txt", "wb") as outf:
    for f in input_files:
        with open(f, "rb") as inf:
            outf.write(inf.read())

