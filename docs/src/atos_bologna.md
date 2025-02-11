Complementary information about DAVAI setup on `aa|ab|ac|ad` HPC machine @ ECMWF/Bologna
========================================================================================

Quick install
-------------

```
module use ~acrd/public/modulefiles
module load davai
```

If you want to specify a fixed version: `module load davai/x.y.z`
To know what version (`x.y.z`) of davai tests to use, cf. https://github.com/ACCORD-NWP/DAVAI-tests/wiki/Versions-of-tests

You can put the first line in your `.bash_profile`, and execute the second only when needed.

---

Pre-requirements (if not already set up)
----------------------------------------

1. Load the required environment for GMKPACK compilation and DAVAI execution. It is **REQUIRED** that you add the following to your `.bash_profile`:
   ```bash
   module purge
   module use /home/acrd/public/modulefiles
   module load intel/2021.4.0 prgenv/intel python3/3.10.10-01 ecmwf-toolbox/2021.08.3.0 davai/master

   # Gmkpack is installed at Ryad El Khatib's
   HOMEREK=~rme
   export GMKROOT=$HOMEREK/public/bin/gmkpack
   # use efficiently filesystems
   export ROOTPACK=$PERM/rootpack
   export HOMEPACK=$PERM/pack
   export GMKTMP=$TMPDIR/gmktmp
   # default compilation options
   export GMKFILE=OMPIIFC2104.AA
   export GMK_OPT=x
   # update paths
   export PATH=$GMKROOT/util:$PATH
   export MANPATH=$MANPATH:$GMKROOT/mani
   ```

2. Ensure permissions to `accord` group (e.g. with `chgrp`) for support, something like:
   ```bash
   for d in $HOME/davai $HOME/pack $SCRATCH/mtool/depot
   do
   mkdir -p $d
   chgrp -R accord $d
   chmod g+s $d
   done
   ```
