# (Re-)Build of executables

The `davai-build` command does 2 sequential things:

1. Fetch sources interactively.
2. Build in each flavour, submitting one batch job building sequentially for each compilation flavour (DP, SP,
   compiler...).

### Build with `gmkpack`

Tasks:

- Fetch sources:

  - from an IAL git ref:
    `gitref2pack` : fetch/pull the sources from the requested Git reference and set one or several incremental `gmkpack`'s pack(s) -- depending on `compilation_flavours` as set in config. The packs are then populated with the set of modifications, from the latest official tag to the contents of your branch (including non-commited modifications).

  - from a bundle:
    `bundle2pack` : fetch the sources of the projects as described in the bundle and set one or several `gmkpack`'s pack(s) -- depending on `compilation_flavours` as set in config -- and populate them with the projects.

- `pack2bin` : compile sources and link necessary executables (i.e. those used in the tests), for each pack flavour.

In case the compilation fails, or if you need to (re-)modify the sources for any reason (e.g. fix an issue):

1. implement corrections in the branch (commited or not)

2. re-run the build:

   ```
   davai-build -e
   ```
   (option `-e` or `--preexisting_pack` assumes the pack already preexists; this is a protection against accidental overwrite of an existing pack. The option can also be passed to `davai-run_xp`)

3. and then if build successful `davai-run_tests`

### Build with ecbundle/cmake

Davai will build IAL and any required dependencies listed in the bundle in a path defined in the platform config file (*e.g.* `DAVAI/src/davai/cli/conf/atos_bologna.ini`) under the key `build` of section `paths`. The build path will be complemented with the experiment name and compilation flavour (*e.g.* `$SCRATCH/davai/build/dv-0004-atos_bologna@user`)


Tasks:

- Fetch sources (`ecbundle create`):

  - from an IAL local repository:
    `bundle_create.py` : uses ecbundle to create a `source` direcotry in the experiment build folder with the sources requestend in the bundle file present in the `bundle/` folder of the IAL repository set by `IAL_dir` in the config file.

  - from a bundle repository:
    `bundle_create.py` : clones the IAL-bundle repository set by the config variables `IAL_bundle_repository` and `IAL_bundle_ref` in the config file and uses ecbundle to create a `source` direcotry in the experiment build folder with the sources requestend in the bundle file present in the IAL-bundle repository.

    
- `pack2bin` : compile sources and link necessary executables (i.e. those used in the tests), for each pack flavour.


Not implemented yet.

