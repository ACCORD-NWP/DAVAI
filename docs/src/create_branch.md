### Create your branch, containing your modifications

To use DAVAÏ to test your IAL contribution to the next development release,
you need to have your code in a IAL Git branch starting from the latest
official release (e.g. `CY48T1` tag for contributions to 48T2, or `CY49`
tag for contributions to 49T1).

In the following the example is taken on a contribution to 48T2:

1. In your repository (e.g. `~/repositories/arpifs` -- make sure it is clean with `git status` beforehand), create your branch:

   ```bash 
   git checkout -b <my_branch> [<starting_reference>]
   ```

   !!! tip "Example" 
       `git checkout -b mary_CY48T1_cleaning CY48T1`
   
   !!! note 
       It is recommended to have explicit branch names with regards to their origin and their owner, hence the legacy branch naming syntax `<user>_<CYCLE>_<purpose_of_the_branch>`

2. Implement your developments in the branch.
    __*It is recommended to find a compromise between a whole development in only one commit, and a large number of very small commits (e.g.  one by changed file).*__
   In case you then face compilation or runtime issues then, but only if you haven't pushed it yet, you can *amend*[^1] the latest commit to avoid a whole series of commits just for debugging purpose.
   !!! note 
       DAVAÏ is able to include non-committed changes in the compilation and testing, when starting from an IAL branch. However, when starting from a bundle, this is not possible.

## And with contributions to OOPS, ectrans & others:

If you have code modifications in repositories other than IAL, the principle is the same,
your changes must be in a branch of these repositories.
Then you need an [IAL bundle](https://github.com/ACCORD-NWP/IAL-bundle) in which to indicate the branch(es)
of the repositories you want to test.
 
[^1]: `git commit –amend`
