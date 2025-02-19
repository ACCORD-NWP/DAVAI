### Investigating a problem

The **usecase** parameter of an experiment (to be set in the
`davai-new_xp` command) determines the span of tests to be generated and
run. Several usecases have been *(or will be)* implemented with various
purposes:

-   `NRV` (default): Non-Regression Validation, minimal set of tests
    that any contribution must pass.

-   `ELP`: Exploration and Localization of Problems, extended set of
    isolated components, to help localizing an issue

-   *`PC`: \[not implemented yet\] set of toy tests ported on
    workstation; the compilation with GNU (usually less permissive than
    vendor compilers) enables to raise issues that might not have been
    seen with NRV/ELP tests.*

### Smaller tests for smaller problems 

To investigate a non-reproducibility or crash issue, the `ELP` usecase
of Davaï can help localizing its context, with a set of more elementary
tests, that run smaller parts of code.

To switch to this mode:

-   create a new experiment with the same arguments but `-u ELP` and go
    in it

-   `davai-run_xp`

Instead of 50$^+$ tests, the ELP mode will provide hundreds of more
elementary and focused tests. For instance, if you had a problem in the
4DVar minimization, you can run the 3 observation operators tests,
observation by observation, and/or a screening, and/or a 3DVar or 4DVar
single-obs minimization, in order to understand if the problem is in a
specific observation operator (which obs type ?), in its direct, TL or
AD version, or in the Variational algorithm, or in the preceding
screening, and so on\...

The user may want, at some point, to run only a subset of this very
large set of tests. In this case, simply open the `conf/ELP.yaml` and
comment (`#`) the launch of the various jobs. To reduce the number of
tests that are innerly looped, e.g. the loop on observation types within
the `*__obstype` jobs: open config file `conf/davai_elp.ini`, look for
the section named after job name and select the obstype(s) to be kept
only in list.

