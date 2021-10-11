# entitypkg

The idea here is to collect decoding and encoding information for Entity Packages.

In this first generation, I'm focused on basic functionality:
* reading entity package files
* writing entity package files

Concerns I'm scoping for a second or third generation include:
* licensing
* finer-grained control over saving records
* versioning

## entityloader.py

There is one function that is used:

* `load(src)` -- load a file, and incorporate it into the local database
	* `src` -- str, path or URL -- identifying a package file

The data is then kept like so:

* `records` -- list of all records, including special keys
    * "special keys" begin with `@` and represent internal marking
        * `@source` -- the specific source (`src`) from `load(src)` that the record was loaded from
        * `@loadtime` -- unix UTC seconds since epoch when package that the record was from was processed
        * `@package` -- the package id for the package that the record was loaded from
* `by_schema` -- an index from `$schema` identifier to records that use that `$schema`
* `by_id` -- an index from `$id` identifier to records (whether facet or link) that have that `$id`
* `links` -- an index from an identifier to link records that mention that identifier
* `sources` -- an index for all records that have the `tag:entitypkg.net,2022:entity-schema:source-v1` schema -- these are facet records that provide the location for further information about an entity

