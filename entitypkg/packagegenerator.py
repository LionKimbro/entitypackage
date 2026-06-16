"""packagegenerator.py  -- create entity package data"""

import time
import json

from constants import *
from memory import *
import util


def output(p, pkgid):
    """Output all records to a package file.
    
    p: str, path  -- file output (overwrite)
    pkgid: str, unique id  -- ID for package outputting
    """
    epkg = {K_FILETYPE: FILETYPE_PACKAGE_V1,
            K_PKGID: pkgid,
            K_RECORDS: []}
    L = epkg[K_RECORDS]
    for rec in records:
        D = {k: v for (k,v) in records.items() if not k.startswith("@")}
        L.append(rec)
