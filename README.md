DAVAI
=====

This project contains:

* the davai command-line interface, to create davai experiments and run them,
* the davai-specific utilities, resources and AlgoComponents for Vortex (plugin)
* the davai tasks templates, jobs sequences and config files
* the documentation

This repository is the result of the merge of:
* the `davai` sub-package from Vortex (1.x)
* the `DAVAI-env` repository (command-line interface)
* the `DAVAI-tests` repository (utilities, tasks & jobs)

Documentation
-------------

Documentation is deployed [here](https://accord-nwp.github.io/DAVAI/).

Installation
------------

DAVAI is deployed on PyPI, or can be git-cloned and installed locally with pip.

It is also preinstalled on MF and ECMWF HPC clusters at MF and ECMWF.

More information on [Installation](docs/src/installation.md) page of documentation.

Quick start
-----------

For a quick start:

1. Prepare an experiment based on version `<v>` of the Davai tests, to validate an IAL Git reference `<r>`:\
   `davai-new_xp <r> [-v <v>] [-h]`\
   Notes:
   * you may need to specify the path to your IAL repository by argument, cf. options with `-h`.
   * to know what version of the tests to use, cf. below. From `CY50`+ onwards, a default version can be infered from
     the IAL repository.
2. Go to the prompted directory of the experiment (ending with `.../dv-<nnnn>-<platform>@<user>/davai/nrv/`) and source
   the associated python virtualenv as prompted:\
   `source venv/bin/activate`
3. Run the tests: `davai-run_xp` and monitor (standard output for the build, then job scheduler).
4. If you need to re-build & re-run tests:
  - `davai-build [-h]`
  - `davai-run_tests [-h]`

More details to be found in the documentation, in particular in case of a multi-repos contribution.

Tests versions and reference experiments
----------------------------------------

From CY50+, a default version of Davai can be found in IAL repo, file `.davai_default_version`.

However, new versions can be recommended, unrelated to changes in the IAL.
For that matter,  it will be referenced [here](docs/src/versions.md)

Dependencies
------------

DAVAI is mainly written in Python. Make sure you have Python3.10 at least.
Python dependencies are included in the `pyproject.toml` file.
They include in particular:
* [_**IAL-build**_](https://github.com/ACCORD-NWP/IAL-build):
  wrappers around `git` and `gmkpack` (and eventually other building tools) to build IAL executables from Git
* [_**IAL-expertise**_](https://github.com/ACCORD-NWP/IAL-expertise):
  tools to analyse automatically the outputs of NWP configurations -- norms, Jo-tables, fields in FA/GRIB files, ...
* [_**EPyGrAM**_](https://github.com/UMR-CNRM/EPyGrAM): a Python library for handling output data from the IAL models;
  it is used here within _IAL-expertise_.
Note that the Vortex package, currently used in version 1.x, is not yet available in these dependencies; cf. below.

It also uses Git, make sure you have a "recent enough" version of it, or some commands may not work properly.
DAVAI works over a number of NWP packages, tools, softwares, that need to be pre-installed on the machine with their own
procedures. These include:

* [_**Vortex**_](https://opensource.umr-cnrm.fr/projects/vortex):
  scripting system used for the definition of tasks (resources, executables launch, ...) and the running
  of the jobs. It embeds a number of necesary-as-well sub-packages.
  
  _Note: A portable version of Vortex, still under progress, will be available and deployed on PyPI soon._

* [_**Gmkpack**_](https://www.umr-cnrm.fr/gmapdoc/spip.php?article79):
  build system for IAL. Documentation is outdated.

These packages may already be pre-installed on MF's HPC or other platforms where DAVAI is already ported.
Cf. the "Local complements" in "Installation" section, in this case.

To install them on a new machine, cf. the projects' installation instructions.

Lexicon
-------

* **DAVAI** = _"Device Aiming at the VAlidation of IAL"_
* **IAL** = IFS-Arpege-LAM

