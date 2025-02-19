### [Setting up a reference version](@id set_ref_version) 

! WORK IN PROGRESS\...

We describe here how to set up a reference version of the tests and an
associated reference experiment, typically for developments based on a
given IAL release to be validated against this release.

For the example, let's consider `CY49` and setting up a `DV49` version
for it, including its reference experiment, to validate the
contributions to `CY49T1`.

1.  Choose an initial version of the tests you want to be used. It may
    probably not be the previous reference one (e.g. `DV48T2` or
    `dev_CY48T1_toT2`), as we may often want to modify or add tests in
    between cycles.

2.  In your development DAVAI-tests repository, make a branch starting
    from this version and check it out, e.g.:\
    `git checkout -b on_49 [<chosen_initial_ref]`

3.  Set the reference experiment:\
    `davai-new_xp CY49 -v on_49 -u ELP --origin <URL of my DAVAI-tests repo>`\
    $\hookrightarrow$ `dv-xxxx-machine@user`\
    Note:

    -   As ELP usecase encompasses NRV, reference experiments should use
        this usecase so it could be used as a reference for both
        usecases.

    -   `--origin <URL...>` to clone that repo in which you created the
        branch

    -   in config of the experiment, set `archive_as_ref = True` : the
        experiment will serve as a reference, so we want to archive its
        results

    -   in config of the experiment, set `ignore_reference = True` : if
        you are confident enough with the test version, it may not be
        useful/relevant to compare the experiment to any reference one.

4.  Run the experiment

5.  Update the `DAVAI-tests` repository:

    -   default config file for this machine (`conf/<machine>.ini`: with
        the name of this experiment as `ref_xpid` (and potentially the
        usecase chosen in minor case as `ref_vconf`)

    -   `README.md`: the table of correspondance of branches and tests

    Then commit, tag (`DV49`) and push:

          git commit -am "Set reference experiment for <machine> as <dv-xxxx-machine@user>"
          git tag DV49
          git push <remote>
          git push <remote> DV49

This way the tests experiment generated using `davai-new_xp -v DV49`
will use this version and be compared to this reference experiment.

