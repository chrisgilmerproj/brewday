# Beer Data

The beer data is split into four sections: Cereals, Hops, Water, and Yeast.
The data is provided in `*.ini` files, one file per data item.  Each item
should have a `[default]` section with a `name` parameter.  That parameter
should be identical to the name of the file, using underscores instead of
spaces or dashes.

An example for Cereals is American Pale 2-row.  The file name should be
`american_pale_2_row.ini` and the default name should be
`name = american pale 2-row`.
