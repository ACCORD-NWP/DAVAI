### Run tests

1. Create your experiment, specifying which version of the tests you need to use:

   ```
   davai-new_xp <my_branch> [-v <tests_version>]
   ```

   !!! tip "Example" 
       ```
       davai-new_xp mary_CY50T1_superdev -v DV50T1
       ```
   
   An experiment with a unique experiment ID is created and prompted as output of the command, together with its path.

   - Starting from CY50T1, the default version of the tests is registered in IAL,
     depending on the basis of your development, so you may not need to specify it.
   - To know what is the version to be used for a given development: See [Versions](versions.md)
   - See `davai-new_xp -h` for more options on this command
   - See Appendix for a more comprehensive approach to tests versioning.

2. Go to the (prompted) experiment directory and load its _**venv**_:

   ```
   source venv/bin/activate
   ```
   
   !!! tip "Useful function to put in your `.bashrc`:"
       ```
       function davai-activate() {
         source ${1:-.}/venv/bin/activate
         }
       ```
       so as to activate an experiment venv using `davai-activate` from within it, or `davai-activate path/to/xp`.
   
   - If you want to set some options differently from the default, open file `conf/davai_nrv.ini` and tune the parameters in the `[DEFAULT]` section.
     The usual tunable parameters are detailed in Section [Other options](otheroptions.md)

   !!! note
       To run `davai-*` commands in an experiment, the venv loaded must be the one of the experiment.

3. Launch the build and tests:

   ```
   davai-run_xp
   ```

   After initializing the Ciboulaï page for the experiment, the command will first run the build of the branch and wait for the executables (that step may take a while, depending on the scope of your modifications, especially with several compilation flavours). Once build completed, it will then launch the tests (through scheduler on HPC).

#### DAVAI editable mode

If you want to be able to modify DAVAI scripts, you need to rely on an editable install of the DAVAI python package.
This is done using option `-e` of `davai-new_xp` command.
It will clone the DAVAI repo in the experiment directory and install it in editable mode in a local venv.

Note that the venv for editable mode can be quite large (>400Mb), so watch out for disk quotas.

If the version you are requesting is not known, you may need to specify the DAVAI origin repository from which to clone/fetch it, using argument `--origin <URL of the remote DAVAI.git>`

## To test a bundle, i.e. a combination of modifications in IAL and other repos

Use command `davai-new_xp_from_bundle`, providing  a bundle refering to your contributions (cf. `-h` for help).

You will have the choice to create a main pack, i.e. recompiling all sources of all packages from scratch, or an incremental pack, relying on a pre-compiled pack based on your branch direct tagged ancestor, and compiling only:
* your modified files and direct dependencies in IAL
* the packages that you specified in the bundle using attribute `incremental_pack`, in bulk, cf. [IAL-bundle doc](https://github.com/ACCORD-NWP/IAL-bundle?tab=readme-ov-file#about-the-bundle-approach).
The choice of main vs. incremental pack is to be set in your experiment config file (`conf/davai_nrv.ini`), attribute `packtype=main|incr`

The rest is identical.
