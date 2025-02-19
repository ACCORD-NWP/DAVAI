## Build options

The choice of a build system is corollary to the versioning of the
tests. However, at time of writing, only `gmkpack` is available within
DAVAÏ.

### Build with `gmkpack`

In the `[gmkpack]` section of config file `conf/davai_.ini`:

-   to make a main pack, instead of an incremental pack\
    $\hookrightarrow$ set `packtype = main`

-   to set the list of compilation flavours to build (a.k.a. compiler
    label/flag)\
    $\hookrightarrow$ use `compilation_flavours`\
    ! if you modify this, you potentially need to modify the
    `compilation_flavour` accordingly in the "families" sections that
    define it, as well as the `programs_by_flavour` that define the
    executables to be built for specific flavours

In the `[gitref2pack]` section:

-   to use a different `$ROOTPACK` (i.e. a different source of ancestor
    packs, for incremental packs)\
    $\hookrightarrow$ use `rootpack`\
    (preferably to modifying the environment variable, so that will be
    specific to that experiment only)

In the `[pack2bin]` section:

-   to make the `pack2bin` task crash more quickly after a
    compilation/link error, or do not crash at all\
    $\hookrightarrow$ set `fatal_build_failure =`

    -   `__finally__` $\Rightarrow$ crash after trying to compile and
        build all executables

    -   `__any__` $\Rightarrow$ crash if compilation fails or right
        after the first executable linking to fail

    -   `__none__` $\Rightarrow$ never == ignore failed builds

-   to re-generate `ics_` files before building\
    $\hookrightarrow$ set `regenerate_ics = True`

-   to (re-)compile local sources with `gmkpack’s` option `Ofrt=2` (i.e.
    `-O0 -check bounds`):\
    $\hookrightarrow$ set `Ofrt = 2`

-   to use more/less threads for compilating (independent) sources files
    in parallel:\
    $\hookrightarrow$ use `threads`

-   to change the list of executables to be built, by default or
    depending on the compilation flavour:\
    $\hookrightarrow$ use `default_programs` and `programs_by_flavour`

Also, any `gmkpack` native variables can be set in the `.bash_profile`,
e.g. `ROOTPACK, HOMEPACK`, etc\... Some might be overwritten by the
config, e.g. if you set `rootpack` in config file.

### Build with \[cmake/makeup/ecbuild\...\]

Not implemented yet.

