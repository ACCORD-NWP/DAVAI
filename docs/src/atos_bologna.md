Complementary information about DAVAI setup on `aa|ab|ac|ad` HPC machine @ ECMWF/Bologna
========================================================================================

Quick install
-------------

Set in your `.bash_profile`:
```bash
module use ~acrd/public/modulefiles
```

then when you need to load davai to create a new testing experiment:
```bash
module load davai/2
```

Note: the version of the tests used in your experiment can be different from the version loaded here.
This `module load ...` is only useful to prepend the PATH with `davai-new_xp*` command(s).

---

Pre-requirements
----------------

1. Recommended environment in your `.bash_profile`:
   ```bash
   module load python3/3.10.10-01
   module load prgenv/intel
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
   If you skip this, support cannot be granted.
