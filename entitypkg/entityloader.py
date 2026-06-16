"""entityloader.py  -- load entity package data"""

import time

import util

from constants import *
from memory import *


# global variables

SRC="SRC"  # source identifier for the package last attempted to be received
PKGID="PKGID"  # cached package ID, for the last package received
TIME="TIME"  # cached time (unix timestamp UTC), for last package received

g = {SRC: None,
     PKGID: None,
     TIME: None}

pkg = {}  # most recently read package; the "working" package


# Functions -- Loading Packages

def report_bad_package(msg):
    raise ValueError("Specified file not a package.", msg, g[SRC])

def receive_package(src):
    """Receive a package file from the Internet or local file system.
    
    Some basic checks are done to be sure that the package is sound:
    * Is it a dictionary?
    * Does it have the schema key I expect?
    * Does it have a package id?
    * Does it have records?
    
    g[SRC] -- before attempting to read, this is set with the src provided
    g[PKGID]  -- upon success, this is updated to the presently received package id
    g[TIME]  -- upon success, this is updated to the current time
    
    This package will be at the center of work for the time being.
    """
    g[SRC] = src
    dl = util.read(src)  # the download
    if not isinstance(dl, dict):
        dl_str = repr(dl)
        beginning = dl_str[:10]
        if len(dl_str) > 10:
            beginning += "..."
        msg = "the JSON data ({}) is not a JSON dictionary".format(beginning)
        report_bad_package(msg)
    pkg.clear()
    pkg.update(dl)  # OK, now I call it pkg
    s1 = K_FILETYPE
    s2 = FILETYPE_PACKAGE_V1
    if K_FILETYPE not in pkg:
        report_bad_package("the JSON data lacks {}: {}".format(s1, s2))
    if pkg[K_FILETYPE] != FILETYPE_PACKAGE_V1:
        report_bad_package("{} is {}, not {}".format(s1, pkg[K_FILETYPE], s2))
    if K_PKGID not in pkg:
        report_bad_package("the JSON data lacks {}".format(K_PKGID))
    if K_RECORDS not in pkg:
        report_bad_package("the JSON data lacks {}".format(K_RECORDS))
    g[PKGID] = pkg[K_PKGID]  # g[PKGID] caches the package's identifier
    g[TIME] = int(time.time())  # g[TIME] demarks the successful receipt of the package


def brand_records():
    for rec in pkg[K_RECORDS]:
        rec[SK_SOURCE] = g[SRC]
        rec[SK_LOADTIME] = g[TIME]
        rec[SK_PACKAGE] = g[PKGID]


def load(src):
    receive_package(src)  # after this call: pkg, g[SRC], g[PKGID], g[TIME]
    brand_records()
    for rec in pkg[K_RECORDS]:
        memory.add(rec)  # performs indexing

