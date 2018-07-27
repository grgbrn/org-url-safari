#!/usr/bin/env python3

import csv
import io
import itertools
import os
import subprocess
import sys

from pprint import pprint

# applescript sometimes returns this 'missing' string instead of urls
MISSING_VALUE = "(missing value)"

def invoke_applescript():
    "Yields tuples (window_number, title, url) from external applescript"

    # applescript is in the same directory as the python script, must set
    # the working directory to be able to invoke this script from a symlink
    script_path = os.path.dirname(os.path.realpath(__file__))

    # the "dwim" args to subprocess.run apparently require py3.7 :/
    out = subprocess.run(["osascript", "-so", "urlsafari.applescript"],
        capture_output=True, text=True, cwd=script_path)
    # print(out)

    out.check_returncode() # throw exception if subprocess fails

    # process tsv blob into structured lines
    reader = csv.reader(io.StringIO(out.stdout), delimiter='\t')
    for line in reader:
        if len(line) == 3:
            yield tuple(line)

def get_structured_tabs(lines, filter_missing=False):
    "Make a dict with int(window_number) -> List(tuple(title, url))"

    def window_number(x):
        return int(x[0])

    out = {}

    # lines must be sorted by your grouping function
    data = sorted(lines, key=window_number)
    for k,g in itertools.groupby(data, window_number):
        out[k] = list(t[1:] for t in g)

    if not filter_missing:
        return out

    # find key of windows that are entirely tabs with MISSING_VALUE urls
    to_remove = [win_num for (win_num, tabvals) in out.items()
                 if all(t[1] == MISSING_VALUE for t in tabvals)]

    # dict removals must occur outside iteration
    for k in to_remove:
        del out[k]

    return out

# simple org output looks like:
"""
* window #1
** page title
http://www.google.com

** another page title
http://www.goggle.com

** something else
http://lobste.rs/foo/bar/baz
"""

def org_dump(tab_data, f):
    "Write structured tab data to an output stream"

    def writeline(l=""):
        f.write(l)
        f.write(os.linesep)

    for k,v in tab_data.items():
        writeline(f"* Window #{k}")
        for title, url in v:
            writeline(f"** {title}")
            writeline(f"{url}")
            writeline()

def main():
    lines = invoke_applescript()
    tabdata = get_structured_tabs(lines, filter_missing=True)
    # pprint(tabdata)
    org_dump(tabdata, sys.stdout)


if __name__ == '__main__':
    main()
