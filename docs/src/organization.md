### Organisation of an experiment

The `davai-new_xp` command-line prepares a "testing experiment"
directory, named uniquely after an incremental number, the platform and
the user.

This testing experiment will consist in:

-   `conf/davai_nrv.ini` : config file, containing parameters such as
    the git reference to test, davai options, historisations of input
    resources to use, tunings of tests (e.g. the input obs files to take
    into account) and profiles of jobs

-   `conf/<USECASE>.yaml` : contains an ordered and categorised list of
    jobs to be ran in the requested usecase.

-   `conf/sources.yaml` : information about the sources to be tested, in
    terms of Git or bundle

-   `venv/` : python venv to be used by the experiment. Either a link to an existing venv, or an actual virtualenv in _editable_ mode

-   a `logs` directory/link will appear after the first execution,
    containing log files of each job.

-   `DAVAI` : in case of _editable_ mode, a clone of the DAVAI repository, checkedout on
    the requested version, used by the venv

-   links to the python packages that are used by the scripts and not pip-packaged yet (only `vortex` remains at present)
