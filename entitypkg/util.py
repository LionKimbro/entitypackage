"""util.py  -- utilities for working with packages"""

import json
import urllib.request


# Functions -- Loading JSON Files

def read(src):
    if src.startswith("http://") or src.startswith("https://"):
        return read_url(src)
    else:
        return read_file(src)

def read_url(url):
    return json.load(urllib.request.urlopen(url))

def read_file(p):
    return json.load(open(p, encoding="utf-8"))


# Functions -- Writing JSON Files

def write(obj, p):
    json.dump(obj, open(p, "w", encoding="utf-8"), indent=2)


