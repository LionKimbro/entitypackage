"""constants.py  -- Entity Package Constants"""


# Constants -- Package Files

K_FILETYPE = "$filetype"
K_PKGID = "$pkgid"
K_RECORDS = "$records"

FILETYPE_PACKAGE_V1 = "tag:entitypkg.net,2022:file-type:package-v1"


# Constants -- Records

K_SCHEMA = "$schema"
K_TYPE = "$type"
K_ID = "$id"

TYPE_LINK = "link"
TYPE_FACET = "facet"


# Constants -- Special Keys

SK_SOURCE = "@source"  # specific source loaded from (URL or local filepath)
SK_LOADTIME = "@loadtime"  # unix utc seconds since epoch; when package began being processed
SK_PACKAGE = "@package"  # package entity id


# Constants -- Special Schema


SCH_SOURCE = "tag:entitypkg.net,2022:entity-schema:source-v1"


