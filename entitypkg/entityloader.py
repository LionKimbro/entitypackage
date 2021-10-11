"""entityloader.py  -- load entity package data"""

import time

from constants import *
import util


# Main Global Memory

records = []  # list of all records, including special keys

by_schema = {}  # idx: $schema to records
by_id = {}  # idx: $id to records
links = {}  # idx: entity id -> link records mentioning the entity id
sources = {}  # idx: entity id -> more info source schema record


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

def index_by_schema():
    for rec in pkg[K_RECORDS]:
        if K_SCHEMA in rec:
            schema = rec[K_SCHEMA]
            by_schema.setdefault(schema, []).append(rec)

def index_by_id():
    for rec in pkg[K_RECORDS]:
        if K_ID in rec:
            eid = rec[K_ID]  # "eid" is used because id is already taken; pronounced "entity ID"
            by_id.setdefault(eid, []).append(rec)

def index_links():
    for rec in pkg[K_RECORDS]:
        if rec[K_TYPE] == TYPE_LINK:
            for eid in linkrec_terminals(rec):
                links.setdefault(eid, []).append(rec)

def index_sources():
    for rec in pkg[K_RECORDS]:
        if rec.get(K_SCHEMA) == SCH_SOURCE:
            sources.setdefault(rec[K_ID], []).append(rec)


def load(src):
    receive_package(src)  # after this call: pkg, g[SRC], g[PKGID], g[TIME]
    brand_records()
    records.extend(pkg[K_RECORDS])
    index_by_schema()
    index_by_id()
    index_links()
    index_sources()


# Functions -- Locating terminal identifiers within link records

def update_list(L, additions):
    """Ordered update."""
    for x in additions:
        if x not in L:
            L.append(x)

def _helper_00(obj):
    "(set aside, to clarify recursing into 'object', not just 'record')"
    seen = []
    if isinstance(obj, dict):
        D = obj
        for (k,v) in D.items():
            if k.startswith("$") or k.startswith("@"):
                continue
            if isinstance(v, str):
                update_list(seen, [v])
            else:
                update_list(seen, _helper_00(v))
    elif isinstance(obj, list):
        L = obj
        for v in L:
            if isinstance(v, str):
                update_list(seen, [v])
            else:
                update_list(seen, _helper_00(v))
    else:
        raise ValueError("I have lost the ability to can")
    return seen

def linkrec_terminals(rec):
    """Return ID terminals for a link block.
    
    The special thing about link blocks, is that their terminals are
    ALL entity identifiers.
    
    This function is a subroutine of index_links, which needs to
    collect the terminals from all link blocks, in order to inventory
    all entity identifiers referenced.
    
    Note that ALL keys that begin with punctuation are IGNORED.
    ex: $schema, $id, @package, ...
    """
    return _helper_00(rec)

