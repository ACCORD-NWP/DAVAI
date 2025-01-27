DAVAI environment & interface
=============================

This project contains:

* the DAVAI command-line tools, to create DAVAI experiments and run them,
* the configuration files to handle general preferences and machine-dependent installation,
* the documentation

Note that the core of DAVAI (tests templates, jobs sequences, config files and launching wrappers) are hosted
separately, in the [DAVAI-tests](https://github.com/ACCORD-NWP/DAVAI-tests) repository.

Installation
------------

* on [`belenos`@MF](docs/src/belenos.md)

* on [`Atos/bologna`@ECMWF](docs/src/atos_bologna.md)

* or to setup your own install:
  * Clone this repository, e.g. in `~/repositories/`:\
    `git clone https://github.com/ACCORD-NWP/DAVAI-env.git`
  * Set paths:
    - `DAVAI_ENV=~/repositories/DAVAI-env`
    - `export PATH=$DAVAI_ENV/bin:$PATH`
    - `export PYTHONPATH=$DAVAI_ENV/src:$PYTHONPATH`
  * Assert dependencies (see below) are satisfied

* If you want to inspect possible customizations:
  - `davai-config show`
  - `davai-config preset_user`

Quick start
-----------

For a quick start:

1. Prepare an experiment based on version `<v>` of the tests, to validate an IAL Git reference `<r>`:\
   `davai-new_xp <r> -v <v> [-h]`\
   (you may need to specify the path to your IAL repository by argument, cf. options with `-h`)\
   To know what version of the tests to use, cf. below.
2. Go to the prompted directory of the experiment (ending with `.../dv-<nnnn>-<platform>@<user>/davai/nrv/`)
3. Run the tests: `davai-run_xp` and monitor (standard output for the build, then job scheduler).
4. If you need to re-build & re-run tests:
  - `davai-build [-h]`
  - `davai-run_tests [-h]`

More details to be found in the documentation, in particular in case of a multi-repos contribution.

Tests versions and reference experiments
----------------------------------------

=> https://github.com/ACCORD-NWP/DAVAI-tests/wiki/Versions-of-tests

Documentation
-------------

The user guide is available [here](https://accord-nwp.github.io/DAVAI-env/).

Dependencies
------------

DAVAI is mainly written in Python3. Make sure you have Python3.6 at least.
It also uses Git, make sure you have a "recent enough" version of it, or some commands may not work properly.
DAVAI works over a number of NWP packages, tools, software, that need to be installed on the machine with their own
procedures. These include:

* [_**Vortex**_](https://opensource.umr-cnrm.fr/projects/vortex):
  scripting system used for the definition of tasks (resources, executables launch, ...) and the running
  of the jobs. It embeds a number of necesary-as-well sub-packages.
* [_**ecbundle**_](https://git.ecmwf.int/projects/ECSDK/repos/ecbundle):
  a utility from ECMWF to gather codes from several repositories, in the required version for each,
  based on a YAML descriptive file (called _bundle_); used in `IAL-build`
* [_**IAL-build**_](https://github.com/ACCORD-NWP/IAL-build):
  wrappers around `git` and `gmkpack` (and eventually other building tools) to build IAL executables from Git
* [_**IAL-expertise**_](https://github.com/ACCORD-NWP/IAL-expertise):
  tools to analyse automatically the outputs of NWP configurations -- norms, Jo-tables, fields in FA/GRIB files, ...
* [_**EPyGrAM**_](https://github.com/UMR-CNRM/EPyGrAM): a Python library for handling output data from the IAL models;
  it is used here within _IAL-expertise_.

These packages may already be pre-installed on MF's HPC or other platforms where DAVAI is already ported.
Cf. the "Local complements" in "Installation" section, in this case.

To install them on a new machine, cf. the projects' installation instructions.

Lexicon
-------

* **DAVAI** = _"Device Aiming at the VAlidation of IAL"_
* **IAL** = IFS-Arpege-LAM

