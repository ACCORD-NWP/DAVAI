# Uget usecase: update namelists for Davai

In this example, we need to update namelists of Davai for the needs of a code modification
(e.g. renaming of a variable, or adding a new block).
Cf. [uget](uget.md) section of this documentation for installation and a more thorough tutorial.

#### Setup a custom catalogue

The "uenv's" or catalogues of static input resources used by Davai are listed in the `conf/davai_nrv.ini` config file
of the experiment.
For instance, in `cy49.davai_specials.02@davai` is to be found a package of namelists.
We first create a local copy of this catalogue with:

```
uget.py hack env cy49.davai_specials.02@davai into cy49.davai_specials.02@@${USER}
```

This will create a local catalogue file under `~/.vortexrc/hack/uget/${USER}/env/`.
Make sure to modify the value in `davai_nrv.ini` to use your local copy.

#### Edit namelists

We then create a local copy of the namelist package listed in this catalogue `49.arpifs@davai.02.nam.tgz@davai`:

```
uget.py hack data 49.arpifs@davai.02.nam.tgz@davai into 49.arpifs@davai.02.nam.tgz@${USER}
```

This creates a tgz file under `~/.vortexrc/hack/uget/${USER}/data/`, which then needs to be unpacked.
Make sure to modify the catalogue file to use your local copy of the namelists.

You then can modify existing namelist files in the unpacked directory.

If your changes are required to run a contribution to IAL, don't forget to provide your catalogue and namelist package
(paths) in your IAL Pull Request.
