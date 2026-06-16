"""memory.py  -- Entity Package Memory

"""


# Global Data -- Main Global Memory

records = []  # list of all records, including special keys

by_schema = {}  # idx: $schema to records
by_id = {}  # idx: $id to records
links = {}  # idx: entity id -> link records mentioning the entity id
sources = {}  # idx: entity id -> more info source schema record


# Global Data -- Indexing

INDEX_NEXT = "INDEX_NEXT"

g = {INDEX_NEXT: 0}


indexing_functions = []


# Fn -- Indexing

def index():
    while g[INDEX_NEXT] < len(records):
        for fn in indexing_functions:
            fn(rec[g[INDEX_NEXT]])
        g[INDEX_NEXT] += 1


def add_index_fn(fn):
    """Add a new index & catch up to the present state of indexing."""
    indexing_functions.append(fn)
    for i in range(g[INDEX_NEXT]):
        fn(rec[i])


# Fn -- Built-in Indexing Functions

def index_by_schema(rec):
    if K_SCHEMA in rec:
        schema = rec[K_SCHEMA]
        by_schema.setdefault(schema, []).append(rec)

def index_by_id(rec):
    if K_ID in rec:
        eid = rec[K_ID]  # "eid" is used because id is already taken; pronounced "entity ID"
        by_id.setdefault(eid, []).append(rec)

def index_links(rec):
    if rec[K_TYPE] == TYPE_LINK:
        for eid in linkrec_terminals(rec):
            links.setdefault(eid, []).append(rec)

def index_sources(rec):
    if rec.get(K_SCHEMA) == SCH_SOURCE:
        sources.setdefault(rec[K_ID], []).append(rec)


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


# Fn -- Module Setup

def setup():
    for fn in [index_by_schema,
               index_by_id,
               index_links,
               index_sources]:
        add_index_fn(fn)


# Fn -- Add Records

def add(rec):
    records.append(rec)
    index()

